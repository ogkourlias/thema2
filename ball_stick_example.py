#!/usr/bin/env python3
"""
Showing an example of the show stick model function in use.
"""

#IMPORTS
from povray import povray, SETTINGS, pdb
from vapory import Scene
from math import pi

#META
__author__ = 'Niels van der Vegt'

def molecule():
    global viagra
    viagra = pdb.PDBMolecule('{}/pdb/viagra.pdb'.format(SETTINGS.AppLocation), center = True)
    viagra.move_offset([0,1,0])
    viagra.scale_atom_distance(1.75)
def scene(step):
    rotate_coo = pi * 2 / 180
    viagra.rotate([0,1,0], rotate_coo)
    viagra.show_stick_model()
    return Scene(povray.default_camera,
                 objects = [povray.default_light] + viagra.povray_molecule)

def main():
    molecule()
    povray.render_scene_to_mp4(scene, time=False)
    
main()

