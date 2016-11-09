#!/usr/bin/env python3

'''
Simple template rendering an ATP molecule originating from a PDB file,
splitting a phosphate (Pi) group resulting in ADP + Pi.

Note: the resulting ADP molecule is not in a realistic conformation.

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2016.2"

import math
from povray import povray, pdb
from vapory import Scene, LightSource

def scene_objects():
    ''' Creates molecule objects and any other pre-calculated data '''
    # Store in the global namespace so the scene() method has access
    global ATP, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 5, -29], 'color', [1, 1, 1],
                              'fade_distance', 15, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ATP = pdb.PDBMolecule('pdb/ATP_ideal.pdb', center=False)
    # Move to the center, and raise a little
    ATP.move_to([0, 6, 0])
    # Rotate so that the N-tail points downwards a bit
    ATP.rotate([0, 1, 1], [0, 1.5, -0.7])


def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    # Create a new molecule by removing a number of atoms from the original molecule
    # This subset molecule is then positioned with the offset parameter
    phosphate = ATP.divide([0, 1, 2, 3, 32, 7, 31], 'phosphate', offset=[0, -4, 0])

    # Show the names of the atoms by using the 'show_label' method. This method requires
    # the active camera to aim the text at the 'viewer' to make it readable.
    ATP.show_label(camera=povray.floor_camera, name=True)
    phosphate.show_label(camera=povray.floor_camera, name=True)

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # lights and in this case, two molecules with its labels.
    return Scene(povray.floor_camera,
                 objects=[povray.default_light, FRONT_LIGHT, povray.checkered_ground] +
                 ATP.povray_molecule + phosphate.povray_molecule,
                 included=['colors.inc'])

if __name__ == '__main__':
    # Create static objects
    scene_objects()

    # Render a single frame
    povray.make_frame(0, scene, time=True)
