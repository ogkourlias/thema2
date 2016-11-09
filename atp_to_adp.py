
'''
Simple template rendering a molecule originating from PDB files.

The animation demonstrates the molecule both rotating and traversing on a
trajectory using the move_to and rotate methods.

NOTE: also shows how to do prototyping using multithreading; see the
prototype.ini configuration file.

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2016.2"

import math
import copy
import numpy as np
from povray import povray, pdb, load_config
from vapory import Scene, Sphere, Text, LightSource, Texture, Pigment, Cylinder, Interior, Finish


def scene_objects():
    ''' Creates molecule objects and any other pre-calculated data '''
    # Store in the global namespace so the scene() method has access
    global VIAGRA, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 5, -29], 'color', [1, 1, 1],
                              'fade_distance', 15, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    VIAGRA = pdb.PDBMolecule('pdb/viagra.pdb', center=False)#, offset=[3, -3, -7])

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    # Place the original molecule
    VIAGRA.move_to([0, 6, 0])
    VIAGRA.rotate([0,1,1], [0, 1, -1.5])
    VIAGRA.show_label(camera=povray.floor_camera, name=True)
    
    # Create a new molecule by removing a number of atoms from the original molecule
    # This subset molecule is then positioned with the offset parameter
    subset = VIAGRA.divide([50, 51, 56, 57, 28, 55, 30, 26, 48, 49], 'subset', offset=[-5, -5, 0])
    subset.show_label(camera=povray.floor_camera, name=True)

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # lights and in this case, two molecules with its labels.
    return Scene(povray.floor_camera,
                 objects=[povray.default_light,
                          FRONT_LIGHT] + VIAGRA.povray_molecule,
                 included=['colors.inc'])

if __name__ == '__main__':
    # Create static objects
    scene_objects()

    # Render a single frame
    povray.make_frame(0, scene, time=True)
