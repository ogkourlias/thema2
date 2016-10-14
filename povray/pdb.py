from vapory import Sphere, Scene, Pigment, Texture, Finish
from povray import povray
from scipy.linalg import expm3, norm
import numpy as np
import sys
import math
import re


class PDBMolecule(object):
    ''' Models a molecule given a PDB file '''

    def __init__(self, pdb_file, center=True, offset=[0,0,0]):
        ''' Parses and renders the molecule given a PDB file '''
        self._parse_pdb(pdb_file)
        self.molecule = pdb_file
        self.offset = np.array(offset)
        if np.count_nonzero(self.offset) > 0:
            self._recenter_molecule()
        self.center = self._center_of_mass()
        if center:
            self.center_molecule()
            self.center = self._center_of_mass()
        print('Created a molecule from "', pdb_file, '" placed at ', 
              np.around(self.center, 2) , ' (centered is ', center, ')', sep='')
        self.povray_molecule = []
        self.model = None

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
        atom = re.findall('[0-9]*([A-Z]+)[0-9]*', element.name)
        if atom:
            atom = atom[0]
        else:
            print(element.name, element.warnings)
        
        return Sphere([element.x, element.y, element.z], 
                      povray.atom_sizes.get(atom, 0.5),
                      Texture(Pigment('color', povray.atom_colors.get(atom, [0, 1, 1])),
                              Finish('phong', 0.8, 'reflection', 0.15)))

    def render_molecule(self, offset=[0, 0, 0]):
        ''' Renders a molecule given a list with atoms '''
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]

    def _center_of_mass(self):
        # Assumes equal weights, not the true center of mass
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

    def move_offset(self, axis, v):
        ''' Move the molecule on the given axis by vector v '''
        # For each given axis, update the value with the axis-specific value from v
        if len(axis.nonzero()) == 0: # move on single axis
            ## TODO
            pass

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

    def rotate(self, axis, theta):
        ''' Rotates the molecule around a given axis with angle theta (radians) '''
        for a in self.atoms:
            # subtract center
            coords = np.array([a.x, a.y, a.z]) - self.center
            rcoords = np.array(self._calc_rotate(axis, theta, coords))
            # update coordinates
            a.x, a.y, a.z = rcoords + self.center
        # Regenerate the molecule
        self.render_molecule()

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


class PDBAtom(object):
    ''' Simple class to parse a single ATOM to retrieve x, y and z coordinates'''
    def __init__(self, string):
        #this is what we need to parse
        #ATOM      1  CA  ORN     1       4.935   1.171   7.983  1.00  0.00      sega
        #XPLOR pdb files do not fully agree with the PDB conventions 
        self.name = string[12:16].strip()
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
