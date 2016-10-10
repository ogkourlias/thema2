'''
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2016.1"

import math
from povray import povray, pdb
from vapory import Scene


def scene_objects():
    ''' Creates molecule objects and any other pre-calculated data '''
    # Store in the global namespace so the scene() method has access
    global ETHANOL, VIAGRA, BENZENE, RAD_PER_SCENE

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ETHANOL = pdb.PDBMolecule('pdb/ethanol.pdb', center=False, offset=[-10, 8, -5])
    VIAGRA = pdb.PDBMolecule('pdb/viagra.pdb', center=False, offset=[3, -3, -7])
    BENZENE = pdb.PDBMolecule('pdb/benzene.pdb', center=False, offset=[0, 8, -5])

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''

    # Rotate the molecules updating its orientation (a persistent modification)
    ETHANOL.rotate([0, 1, 0], RAD_PER_SCENE)
    VIAGRA.rotate([1, 0, 0], RAD_PER_SCENE)
    BENZENE.rotate([0, 0, 1], RAD_PER_SCENE)

    # Return the scene for rendering
    print('@Step: ', step)

    # Combine molecule objects (an object.povray_molecule is a list of atoms, they need
    # to be concatenated to be added to the scene)
    molecules = ETHANOL.povray_molecule + VIAGRA.povray_molecule + BENZENE.povray_molecule

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # light(s) and in this case, molecules too.
    return Scene(povray.default_camera,
                 objects=[povray.default_light] + molecules,
                 included=['colors.inc'])


if __name__ == '__main__':
    # Create objects for the scene (i.e. parse PDB files)
    scene_objects()

    # Render single frame as PNG file
    #povray.make_frame(1, scene, time=False)

    # Or, render as a GIF file (low quality)
    #povray.render_scene_to_gif(scene, time=True)

    # Or, render as an MP4 movie
    povray.render_scene_to_mp4(scene, time=True)
