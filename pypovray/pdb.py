"""
Module for creating and managing Povray molecules originating from
a PDB file.
"""

import math
import re
import numpy as np
from vapory.vapory import Sphere, Cylinder, Text, Pigment, Texture, Finish, Intersection, Union
from pypovray import SETTINGS, logger
from pypovray.models import atom_colors, atom_sizes, text_model
from scipy.linalg import expm, norm


class PDBMolecule(object):
    """
    Models a molecule for rendering using Povray given a PDB file.
    """
    def __init__(self, pdb_file, center=True, offset=[0, 0, 0], atoms=False, model=None):
        """
        Parses and renders the molecule given a PDB file.
        """
        # If a list of atoms is provided, use these instead of a PDB file
        # This allows dividing the molecule in segments, see divide().
        if atoms:
            self.atoms = atoms
        else:
            self._parse_pdb(pdb_file)
            self.povray_molecule = []

        self.molecule = pdb_file
        self.warnings = set()

        # If an offset is provided, apply this
        self.offset = np.array(offset)
        if np.count_nonzero(self.offset) > 0:
            self._recenter_molecule()

        # Center the molecule based on the 'pseudo' center of mass
        self.center = self._center_of_mass()
        if center:
            self.center_molecule()
            self.center = self._center_of_mass()
        logger.info("Created a molecule from '%s' placed at [%s] (centered is %d)",
                    pdb_file, ', '.join([str(coord) for coord in np.around(self.center, 2)]), center)

        # Required for the attachments.
        self.show_name = False
        self.show_index = False
        self.camera = None
        self.show_sticks = False

        self.model = model
        self.render_molecule(offset)

    def _parse_pdb(self, fname):
        """
        Read in a PDB file and create an atom object for each ATOM definition.
        """
        self.atoms = []
        with open(fname) as pdbfile:
            for line in pdbfile:
                if line.startswith('ATOM') | line.startswith('HETATM'):
                    # Create a new PDBAtom object using the line's values.
                    self.atoms.append(PDBAtom(line))
                elif line.startswith('CONECT'):
                    # Extract the atom's index and parse its bonds, if any.
                    atom = int(line[6:11]) - 1
                    self.atoms[atom].parse_bonds(line, self.atoms)

    def _recenter_molecule(self):
        """
        Moves the molecule by a given offset when instantiating the object
        """
        for atom in self.atoms:
            atom.x += self.offset[0]
            atom.y += self.offset[1]
            atom.z += self.offset[2]

    def _get_atom(self, element, offset):
        """
        Creates a Povray Sphere object representing an atom
        """
        if element.element not in atom_colors:
            self.warnings.add(element.element)

        if self.model:
            atom_model = self.model
        else:
            atom_model = Texture(Pigment('color', atom_colors.get(element.element, [0, 1, 1])),
                                 Finish('phong', 0.9, 'reflection', 0.1))

        return Sphere([element.x + offset[0], element.y + offset[1], element.z + offset[2]],
                       atom_sizes.get(element.element, 0.5), atom_model)

    def render_molecule(self, offset=[0, 0, 0]):
        """
        Renders a molecule given a list with atoms.
        """
        # Declare a storage list for labels and stick-model sticks.
        self.attachments = []

        if self.show_sticks:
            self.show_stick_model()
        if self.show_name:
            self.show_label(camera=self.camera, name=True)
        if self.show_index:
            self.show_label(camera=self.camera, name=False)

        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]
        # Warn if unknown atoms are found.
        if len(self.warnings) > 0:
            if any(element == '' for element in self.warnings):
                logger.warning("The PDB file is missing atom names!")
            else:
                logger.warning("The following atoms are not defined in the 'models' module: %s",
                               ", ".join(self.warnings))

            self.warnings = set()

    def _update_render(self, offset=[0, 0, 0]):
        """
        Updates the render without re-rendering attachments.
        """
        # Update the render of the molecule's atoms.
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]
        # Add previous attachments to the newly rendered molecule.
        self.povray_molecule += self.attachments

    def _center_of_mass(self):
        """
        Calculates the 'center of mass' for the molecule
        Note: assumes equal weights, not the true center of mass
        """
        x, y, z = 0, 0, 0
        for atom in self.atoms:
            x += atom.x
            y += atom.y
            z += atom.z

        return np.array([x/len(self.atoms), y/len(self.atoms), z/len(self.atoms)])

    def center_molecule(self):
        """
        Centers the molecule by subtracting the calculated COM value.
        """
        curr_center = self._center_of_mass()
        # Center each atom.
        for atom in self.atoms:
            atom.x -= curr_center[0]
            atom.y -= curr_center[1]
            atom.z -= curr_center[2]

    def set_model(self, model):
        """
        Set render specific options for the atoms (i.e. reflection).
        """
        self.model = model

    def move_offset(self, v):
        """
        Move the molecule - and thus each individual atom - on the given axes by vector v.
        """
        for atom in self.atoms:
            atom.x += v[0]
            atom.y += v[1]
            atom.z += v[2]

        # Calculate the new center of mass.
        self.center = self._center_of_mass()

        # Regenerate the molecule.
        self.render_molecule()

    def move_to(self, pos):
        """
        Move the center of the molecule to the position pos.
        """
        offset = np.array(pos) - self.center

        # Move each atom.
        for atom in self.atoms:
            atom.x += offset[0]
            atom.y += offset[1]
            atom.z += offset[2]

        # Calculate the new center of mass.
        self.center = self._center_of_mass()

        # Regenerate the molecule.
        self.render_molecule()

    def rotate(self, axis, theta):
        """
        Rotates the molecule around a given axis with angle theta (radians).
        """
        for atom in self.atoms:
            # Subtract center.
            coords = np.array([atom.x, atom.y, atom.z]) - self.center
            rcoords = np.array(self._calc_rotate(axis, theta, coords))
            # Update coordinates.
            atom.x, atom.y, atom.z = rcoords + self.center

        # Regenerate the molecule.
        self.render_molecule()

    def rotate_by_step(self, axis, theta, step, time=False):
        """
        Rotates the molecule around a given axis with angle theta (radians)
        but always resets the molecule to its original rotation first which
        makes it usable in a multi-threaded environment.
        """
        # If step is in seconds, divide by the FrameTime to get the integer (actual) step.
        if time:
            step = int(step/eval(SETTINGS.FrameTime))

        for atom in self.atoms:
            # subtract center.
            coords = np.array([atom.x, atom.y, atom.z]) - self.center

            # Reset the coordinates.
            reset = np.array(self._calc_rotate(axis, -(theta*(step)), coords))
            atom.x, atom.y, atom.z = reset

            # Calculate rotation coordinates.
            rcoords = np.array(self._calc_rotate(axis, theta*(step+1), coords))

            # Update coordinates.
            atom.x, atom.y, atom.z = rcoords + self.center

        # Regenerate the molecule.
        self.render_molecule()

    def scale_atom_distance(self, scale=1, revert=False):
        """
        Simple function that iterates through all atoms and scales them using
        the given scale parameter. The revert parameter functions as a return
        to the atom's original coordinates and resets the atoms' previous
        scaling factor.
        """
        for atom in self.atoms:
            # Store coordinates temporarily in numpy array.
            coordinates = np.array([atom.x, atom.y, atom.z])

            if revert:
                # Calculate the scaling factor needed to revert the coordinates
                # back to their original van der Waals radii.
                scale_to_original = 1 / atom.scale
                # Place coordinates back on their original position.
                coordinates *= scale_to_original
                # Reset atom scaling factor to 1.
                atom.scale = 1

            # Set the atom's scaled coordinates.
            atom.x, atom.y, atom.z = coordinates * scale
            # Update atom's scaling factor with current scaling factor.
            atom.scale *= scale

        self.render_molecule()

    def show_label(self, camera, name=False):
        """
        Shows a label of each atom in the list of atoms by printing either
        its index or atom name on the 'front' of the atom. The position
        of the label depends on the camera position; it always faces the
        camera so that it's readable.
        """
        # Storing all label Povray objects.
        labels = []
        # Get the coordinates of the camera.
        # TODO: does not work for all camera's!
        camera_coords = np.array(camera.args[1])

        for i, atom in enumerate(self.atoms):
            # Default atom size (for undefined atoms) is 0.5.
            atom_radius = atom_sizes.get(atom.name, 0.5)
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

            # Defining the two vectors; Atom center (A) and camera viewpoint (B).
            A = np.array([atom.x, atom.y, atom.z])
            B = np.array(camera_coords)
            BA = B - A  # Vector B->A
            d = math.sqrt(sum(np.power(BA, 2)))  # Euclidean distance between the vectors.
            BA = BA / d  # Normalize by its length; BA / ||BA||.
            # Here we find a point on the vector B->A with a distance of 'scale' from the
            # atom center towards the camera (outside of the atom).
            scale = atom_radius * 1.2
            N = A + scale * BA # Scale and add to A

            # Now that we have the distance, we calculate the angles facing the camera.
            x1, y1, z1 = A
            x2, y2, z2 = B
            y_angle = math.degrees(math.atan2(x1 - x2, z1 - z2))
            x_angle = math.degrees(math.atan2(y1 - y2, z1 - z2))

            # Correct for the letter size since text is never centered and place
            # the text in front of the atom to make it visible (emboss).
            N -= letter_offset
            emboss = -0.15

            # 'rotate' rotates the text to the camera and 'translate' positions the text
            # on the vector originating from the camera viewpoint to the atom center.
            # The scaling parameter scales (reduces) the text size.
            text = Text('ttf', '"timrom.ttf"', '"{}"'.format(str(label)), 1, 0,
                        'scale', [0.5, 0.5, 0.5], text_model,
                        'rotate', [-x_angle, y_angle, 0], 'translate', N)

            # Create a sphere with the same position and dimensions as the atom
            sphere = Sphere(A, atom_radius, text_model)
            # Add the intersection of this sphere and the text to the labels
            labels.append(Intersection(sphere, text, 'translate', [0, 0, emboss]))

        # Add the labels to atoms.
        self.attachments += labels
        # Update the rendering.
        self._update_render()

    def show_stick_model(self, stick_radius=0.5):
        """
        Turns the space filling model into a stick and ball model by placing
        cylinders between two bonded atoms.

        It is advised to first scale the molecule a certain amount such that
        bonded atoms to not intersect.
        """
        # Declaring container for bond cylinders.
        sticks = []

        # Iterate through the molecule's atoms.
        for index, atom in enumerate(self.atoms):
            # Get the atom's radius from the atom's modelling guidelines.
            atom_radius = atom_sizes.get(atom.name, 0.5)
            # Get a model that follows the atom's styling guidelines.
            stick_a_model = Texture(Pigment('color', atom_colors.get(atom.name, [0, 1, 1])),
                                    Finish('phong', 0.3, 'reflection', 0.1))

            # Iterate through all the atom's bonds.
            for bond_atom in atom.bonds:
                # Get the bonded atom's radius from the atom's modelling guidelines.
                bond_atom_radius = atom_sizes.get(bond_atom.name, 0.5)
                # Get a model that follows the bonded atom's styling guidelines.
                stick_b_model = Texture(Pigment('color', atom_colors.get(bond_atom.name, [0, 1, 1])),
                                        Finish('phong', 0.3, 'reflection', 0.1))

                # Define two points corrosponding to the atoms' centers.
                A = np.array([atom.x, atom.y, atom.z])
                B = np.array([bond_atom.x, bond_atom.y, bond_atom.z])

                # Define a vector along these the atoms' centers.
                V = B - A
                # Calculate the magnitude of this vector, ||V||.
                magnitude = np.sqrt(sum(np.power(V, 2)))
                # Normalize the vector so that we can move along it using a defined distance, V / ||V||.
                unit_vector = V / magnitude

                # In this case we want to find the point where our vector intersects with atom A
                # or atom B their radii respectively. We simply move the distance of the atom's
                # radius along the vector.
                A_intersect = A + (atom_sizes.get(atom.name, 0.5) * unit_vector)
                B_intersect = B - (atom_sizes.get(bond_atom.name, 0.5) * unit_vector)
                # Calculate the 'true' midpoint between the spheres: the middle point of the
                # space in between the two atoms.
                midpoint = (A_intersect + B_intersect) / 2

                # Create the cylinders ranging from the midpoint to each of the atoms' centers.
                stick_a = Cylinder(midpoint, A, stick_radius, stick_a_model)
                stick_b = Cylinder(midpoint, B, stick_radius, stick_b_model)

                # Union the sticks to form one cyclinder representing a single bond, then add it
                # to the list of bonds/sticks.
                sticks.append(Union(stick_a, stick_b))

        # Add sticks to the list of objects to render.
        self.attachments += sticks
        # Update the rendering.
        self._update_render()

    def divide(self, atoms, name, offset=[0, 0, 0]):
        """
        Given a list of atom indices, split the current molecule into two molecules
        where the original one is reduced and a new one is built with the defined
        atoms
        """
        # Define a new molecule from the given atoms.
        molecule = [self.atoms[i] for i in atoms]

        # Remove the atom's bonds with atoms it is no longer connected to (atoms
        # not found within the new molecule).
        for atom in molecule:
            for bond in atom.bonds:
                if bond not in molecule:
                    # Remove bonds on both ends.
                    atom.bonds.remove(bond)
                    bond.bonds.remove(atom)

        # Remove atoms from original molecule (self).
        for index in sorted(atoms, reverse=True):
            del self.atoms[index]

        # Regenerate the reduced molecule.
        self.render_molecule()

        # Return a new PDBMolecule.
        return PDBMolecule(name, center=False, offset=offset, atoms=molecule)

    def _calc_rotate(self, axis, theta, v):
        """
        Calculates the new coordinates for a rotation
        axis:  vector, axis to rotate around
        theta: rotation in radians
        v:     vector, original object coordinates
        """
        # Compute the matrix exponential using Taylor series
        M0 = expm(np.cross(np.eye(3), axis/norm(axis)*theta))
        # Multiply the rotation matrix with the vector v
        return np.dot(M0, v)

    def __repr__(self):
        pass

    def __str__(self):
        """
        Provides an overview of the molecule
        For each atom the index in the self.atoms list, its name and
        current coordinates are shown.
        """
        curr_center = np.around(self._center_of_mass(), 2)
        header = ('\nOverview for the molecule read from {}\n'.format(self.molecule) +
                  '=' * 54 + '\nIdx\t\tAtom\t\tx\ty\tz\n')
        footer = ('=' * 54 +
                  '\nMolecule is currently centered at {}'.format(curr_center))

        structure = []
        for idx, atm in enumerate(self.atoms):
            structure.append('{}:\t\t{}\t\t{}\t{}\t{}\t'.format(idx, atm.element,
                                                                format(atm.x, '.2f'),
                                                                format(atm.y, '.2f'),
                                                                format(atm.z, '.2f')))
        return '{}{}\n{}\n'.format(header, '\n'.join(structure), footer)


class PDBAtom(object):
    """
    Class to parse a single ATOM string to extract atom name/element, x, y and
    z coordinates and possibly bonded atoms.
    """
    def __init__(self, string):
        """
        Constructor that creates a PDBAtom object given values contained in a
        PDB ATOM string. The string is parsed in various ways and it's key values
        are stored within this atom.

        Example of a input (the ATOM string) to be parsed:
        ATOM      1  CA  ORN     1       4.935   1.171   7.983  1.00  0.00      sega

        XPLOR pdb files do not fully agree with the PDB conventions.
        """
        # Atom name parsing.
        name = string[12:16].strip()
        self.name = ''.join(re.findall('[0-9]*([A-Za-z]+)[0-9]*', name))

        # Coordinate parsing.
        self.scale = 1
        self.x = float(string[30:38].strip())
        self.y = float(string[38:46].strip())
        self.z = float(string[46:54].strip())

        # Containers for bonds and warnings.
        self.bonds = []
        self.warnings = []

        # Element parsing using parse_element function.
        self.element = self._parse_element(string)

    def _parse_element(self, string):
        """
        Parses an atom's element given a PDB ATOM string.
        Should the atom's element not be recognized (i.e. it is not given) then
        the atom's chemical element is guessed from its name.
        """
        if len(string) < 78:
            element = string[12:16].strip()
            self.warnings.append('Chemical element name guessed ' +
                                 'to be "%s" from atom name "%s"' % (element, self.name))
        else:
            element = string[76:78].strip()

        return element

    def parse_bonds(self, string, atoms):
        """
        Function to parse bonded atoms, using CONECT lines from a PDB file.

        Extracts all values excluding the CONECT identifier and the current
        atom, then converts these values to integers. The corrosponding
        atom for each value is then found and added to the list of bonded atoms.

        Example of input (the CONECT string) to be parsed:
        CONECT    1    2    3    4    8
        """
        parsed_values = [int(i) - 1 for i in string.split()[2:]]
        self.bonds = [atoms[bond] for bond in parsed_values]
