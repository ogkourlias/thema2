from vapory import Sphere, Scene, Text, Pigment, Texture, Finish, Intersection
from povray import povray, SETTINGS
from scipy.linalg import expm3, norm
import numpy as np
import sys
import math
import re


class PDBMolecule(object):
    ''' Models a molecule given a PDB file '''

    def __init__(self, pdb_file, center=True, offset=[0,0,0], atoms=False, model=None):
        ''' Parses and renders the molecule given a PDB file '''

        # If a list of atoms is provided, use these instead of a PDB file
        # This allows dividing the molecule in segments, see divide()
        if atoms:
            self.atoms = atoms
        else:
            self._parse_pdb(pdb_file)
            self.povray_molecule = []

        # Molecule name
        self.molecule = pdb_file
        self.warnings = set()
        # If an offset is provided, apply this
        self.offset = np.array(offset)
        if np.count_nonzero(self.offset) > 0:
            self._recenter_molecule()
        self.center = self._center_of_mass()
        
        # Center the molecule based on the 'pseudo' center of mass
        if center:
            self.center_molecule()
            self.center = self._center_of_mass()
        print('Created a molecule from "', pdb_file, '" placed at ', 
              np.around(self.center, 2) , ' (centered is ', center, ')', sep='')

        # Required for the labels
        self.show_name = False
        self.show_index = False
        self.camera = None
        
        self.model = model
        self.render_molecule(offset)

    def _parse_pdb(self, fname):
        ''' Read in a PDB file and create an atom object for each ATOM definition '''
        with open(fname) as pdbfile:
            self.atoms = [PDBAtom(atom) for atom in pdbfile if atom.startswith('ATOM') |
                          atom.startswith('HETATM')]

    def _recenter_molecule(self):
        ''' Moves the molecule by a given offset when instatiating the object '''
        for atom in self.atoms:
            atom.x += self.offset[0]
            atom.y += self.offset[1]
            atom.z += self.offset[2]

    def _get_atom(self, element, offset):
        ''' Creates a Povray Sphere object representing an atom '''
        # Check if atom is defined in the models module
        if element.name not in povray.atom_colors:
            self.warnings.add(element.name)

        if self.model:
            atom_model = self.model
        else:
            atom_model = Texture(Pigment('color', povray.atom_colors.get(element.name, [0, 1, 1])),
                                 Finish('phong', 0.9, 'reflection', 0.1))
        return Sphere([element.x + offset[0], element.y + offset[1], element.z + offset[2]], 
                      povray.atom_sizes.get(element.name, 0.5), atom_model)

    def render_molecule(self, offset=[0, 0, 0]):
        ''' Renders a molecule given a list with atoms '''
        if self.show_name:
            self.show_label(camera=self.camera, name=True)
        if self.show_index:
            self.show_label(camera=self.camera, name=False)
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]

        # Warn if unknown atoms are found
        if len(self.warnings) > 0:
            print("Warning; the following atoms are not defined in the 'models.py' module: \n\t'",
                  ", ".join(self.warnings), "'\t", sep='')
            # Clear warnings
            self.warnings=set()

    def _update_render(self, offset=[0, 0, 0]):
        ''' Updates the render without re-applying the labels '''
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]

    def _center_of_mass(self):
        # Assumes equal weights, *not* the true center of mass
        x,y,z = 0, 0, 0
        for atom in self.atoms:
            x += atom.x
            y += atom.y
            z += atom.z
        return np.array([x/len(self.atoms), y/len(self.atoms), z/len(self.atoms)])
    
    def center_molecule(self):
        ''' Centers the molecule by sutracting the calculated com value '''
        curr_center = self._center_of_mass()
        for atom in self.atoms:
            atom.x -= curr_center[0]
            atom.y -= curr_center[1]
            atom.z -= curr_center[2]

    def set_model(self, model):
        ''' Set render specific options for the atoms (i.e. reflection) '''
        self.model = model

    def move_offset(self, pos):
        ''' Move the molecule - and thus each individual atom - on the given axes by vector v '''
        # Move on multiple axes
        for atom in self.atoms:
            atom.x += pos[0]
            atom.y += pos[1]
            atom.z += pos[2]

        # Calculate the new center of mass
        self.center = self._center_of_mass()

        # Regenerate the molecule
        self.render_molecule()

    def move_to(self, pos):
        ''' Move the center of the molecule to the position pos '''
        # Calculate the offset to move each atom with
        offset = np.array(pos) - self.center

        # Move each atom
        for atom in self.atoms:
            atom.x += offset[0]
            atom.y += offset[1]
            atom.z += offset[2]

        # Calculate the new center of mass
        self.center = self._center_of_mass()

        # Regenerate the molecule
        self.render_molecule()

    def rotate(self, axis, theta):
        ''' Rotates the molecule around a given axis with angle theta (radians) '''
        for atom in self.atoms:
            # subtract center
            coords = np.array([atom.x, atom.y, atom.z]) - self.center
            rcoords = np.array(self._calc_rotate(axis, theta, coords))
            # update coordinates
            atom.x, atom.y, atom.z = rcoords + self.center
        # Regenerate the molecule
        self.render_molecule()

    def rotate_by_step(self, axis, theta, step, time=True):
        ''' Rotates the molecule around a given axis with angle theta (radians) 
            but always resets the molecule to its original rotation first which
            makes it usable in a multi-threaded environment. '''

        # If step is in seconds, divide by the FrameTime to get the integer (actual) step
        if time:
            step = int(step/eval(SETTINGS.FrameTime))

        for atom in self.atoms:
            # subtract center
            coords = np.array([atom.x, atom.y, atom.z]) - self.center

            # Reset the coordinates 
            reset = np.array(self._calc_rotate(axis, -(theta*(step)), coords))
            atom.x, atom.y, atom.z = reset

            # Calculate rotation coordinates
            rcoords = np.array(self._calc_rotate(axis, theta*(step+1), coords))

            # update coordinates
            atom.x, atom.y, atom.z = rcoords + self.center

        # Regenerate the molecule
        self.render_molecule()

    def show_label(self, camera=povray.default_camera, name=False):
        ''' Shows a label of each atom in the list of atoms by printing either
            its index or atom name on the 'front' of the atom. The position
            of the label depends on the camera position; it always faces the
            camera so that it's readable. '''
        # Storing all label Povray objects
        labels = []
        # Get the coordinates of the camera
        # TODO: does not work for all camera's!
        camera_coords = np.array(camera.args[1])

        for i, atom in enumerate(self.atoms):
            # Default atom size (for undefined atoms) is 0.5
            atom_radius = povray.atom_sizes.get(atom.name, 0.5)
            if name:
                label = atom.name
                letter_offset = np.array([0.15 * len(label), 0.13 * len(label), 0.0])
                self.show_name = True
            else:
                label = i
                ndigits = len(str(abs(label)))
                letter_offset = np.array([0.15 * ndigits, 0.13 * ndigits, 0.0])
                self.show_index = True
            self.camera = camera

            # Defining the two vectors; Atom center (A) and camera viewpoint (B)
            A = np.array([atom.x, atom.y, atom.z])
            B = np.array(camera_coords)
            BA = B-A # Vector B->A
            d = math.sqrt(sum(np.power(BA, 2))) # Euclidean distance between the vectors
            BA = BA / d # Normalize by its length; BA / ||BA||
            # Here we find a point on the vector B->A with a distance of 'scale' from the
            # atom center towards the camera (outside of the atom).
            scale = atom_radius * 1.2
            N = A + scale * BA # Scale and add to A

            # Now that we have the distance we calculate the angles facing the camera
            x1, y1, z1 = A
            x2, y2, z2 = B
            yangle = math.degrees(math.atan2(x1 - x2, z1 - z2))
            xangle = math.degrees(math.atan2(y1 - y2, z1 - z2))

            # Correct for the letter size since text is never centered and place
            # the text in front of the atom to make it visible
            N -= letter_offset
            emboss = -0.05

            # 'rotate' rotates the text to the camera and 'translate' positions the text
            # on the vector originating from the camera viewpoint to the atom center.
            # The scaling parameter scales (reduces) the text size
            text = Text('ttf', '"timrom.ttf"', '"{}"'.format(str(label)), 1, 0,
                        'scale', [0.5, 0.5, 0.5], povray.text_model,
                        'rotate', [-xangle, yangle, 0], 'translate', N)

            # Create a sphere with the same position and dimensions as the atom
            sphere = Sphere(A, atom_radius, povray.text_model)
            # Add the intersection of this sphere and the text to the labels
            labels.append(Intersection(sphere, text, 'translate', [0, 0, emboss]))

        # Update the rendering
        self._update_render()
        # Add the labels to atoms
        self.povray_molecule += labels

    def divide(self, atoms, name, offset=[0,0,0]):
        ''' Given a list of atom indices, split the current molecule into two molecules
            where the original one is reduced and a new one is built with the defined
            atoms '''
        # Create a list with all requested atoms
        molecule = [self.atoms[i] for i in atoms]

        # Remove atoms from self
        for index in sorted(atoms, reverse=True):
            del self.atoms[index]

        # Regenerate the reduced molecule
        self.render_molecule()

        # Return a new PDBMolecule
        return PDBMolecule(name, center=False, offset=offset, atoms=molecule)

    def _calc_rotate(self, axis, theta, v):
        ''' Calculates the new coordinates for a rotation
            axis:  vector, axis to rotate around
            theta: rotation in radians
            v:     vector, original object coordinates
        '''
        # Compute the matrix exponential using Taylor series
        M0 = expm3(np.cross(np.eye(3), axis/norm(axis)*theta))
        # Multiply the rotation matrix with the 
        return np.dot(M0, v)

    def __repr__(self):
        pass

    def __str__(self):
        ''' Provides an overview of the molecule
            For each atom the index in the self.atoms list, its name and 
            current coordinates are shown. '''
        curr_center = np.around(self._center_of_mass(), 2)
        header = ('\nOverview for the molecule read from {}\n'.format(self.molecule) +
                  '=' * 54 + '\nIdx\t\tAtom\t\tx\ty\tz\n')
        footer = ('=' * 54 +
                  '\nMolecule is currently centered at {}'.format(curr_center))

        structure = []
        for idx, atm in enumerate(self.atoms):
            structure.append('{}:\t\t{}\t\t{}\t{}\t{}\t'.format(idx, atm.name,
                                                                format(atm.x, '.2f'),
                                                                format(atm.y, '.2f'),
                                                                format(atm.z, '.2f')))
        return '{}{}\n{}\n'.format(header, '\n'.join(structure), footer)


class PDBAtom(object):
    ''' Simple class to parse a single ATOM to retrieve x, y and z coordinates'''
    def __init__(self, string):
        #this is what we need to parse
        #ATOM      1  CA  ORN     1       4.935   1.171   7.983  1.00  0.00      sega
        #XPLOR pdb files do not fully agree with the PDB conventions 
        name = string[12:16].strip()
        self.name = ''.join(re.findall('[0-9]*([A-Za-z]+)[0-9]*', name))
        self.x = float(string[30:38].strip())
        self.y = float(string[38:46].strip())
        self.z = float(string[46:54].strip())
        self.warnings = []
        if len(string) < 78:
            self.element = self.name[0]
            self.warnings.append('Chemical element name guessed ' +\
                                 'to be %s from atom name %s' % (self.element, self.name))
        else:
            self.element = string[76:78].strip()
