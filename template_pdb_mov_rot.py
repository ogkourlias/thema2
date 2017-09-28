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
__version__ = "2017.2"

import math
import copy
from pypovray import pypovray, pdb, load_config, models
from vapory.vapory import Scene, LightSource

ETHANOL = RAD_PER_SCENE = FRONT_LIGHT = None


def scene_objects():
    """ Creates molecule objects and any other pre-calculated data """
    global ETHANOL, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 14, -28], 'color', [1, 0.8, 0.4],
                              'fade_distance', 6, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ETHANOL = pdb.PDBMolecule('pdb/ethanol.pdb', center=False, offset=[-10, 8, -5])


def scene(step):
    """ Returns the scene at step number (1 step per frame) """

    # The Ethanol molecule is moved on a trajectory representing a 'figure 8' or the infinity
    # symbol by calculating the x- and y-coordinates using the lemniscate of Bernoulli.
    scale = 25 / (3 - math.cos(2*step))
    x = scale * math.cos(step)
    y = scale * math.sin(2*step) / 2

    # Copying the full molecule - only needed for multithreading
    # This is required for multithreading
    ethanol = copy.deepcopy(ETHANOL)

    # Move the molecule to the calculated coordinates
    ethanol.move_to([x, y, -5])
    # Rotate the molecule on x- and y-axes
    # NOTE: rotate does NOT work when using a thread-pool,
    # use the molecule.rotate_by_step method instead
    ethanol.rotate_by_step([1, 1, 0], RAD_PER_SCENE, step, time=True)
    ethanol.show_label(camera=models.default_camera, name=True)
    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # lights and in this case, a molecule.
    return Scene(models.default_camera,
                 objects=[models.default_light, FRONT_LIGHT] + ethanol.povray_molecule,
                 included=['colors.inc'])


if __name__ == '__main__':
    # Load the prototyping settings instead of the default
    pypovray.SETTINGS = load_config('prototype.ini')
    # Adjust a loaded setting
    pypovray.SETTINGS.Duration = 6.3
    # Create static objects
    scene_objects()

    # Render as an MP4 movie
    pypovray.render_scene_to_mp4(scene)

    # Timing for running the current simulation including creating the movie:
    #  |  Single-thread (s)  |  Multi-threaded (s) |
    #  |---------------------|---------------------|
    #  |       101.561       |       16.341        |
    #  |---------------------|---------------------|
