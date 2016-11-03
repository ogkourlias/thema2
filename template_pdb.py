'''
Simple template rendering a number of molecules originating from PDB files.

It also demonstrates the usage of different configuration files to influence
the rendering (use -h to see how).

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2016.2"

import sys
import math
import argparse
from povray import povray, pdb, SETTINGS, load_config
from vapory import Scene, LightSource


def scene_objects():
    ''' Creates molecule objects and any other pre-calculated data '''
    # Store in the global namespace so the scene() method has access
    global ETHANOL, VIAGRA, BENZENE, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 14, -28], 'color', [1, 0.8, 0.4],
                              'fade_distance', 6, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ETHANOL = pdb.PDBMolecule('pdb/ethanol.pdb', center=False, offset=[-10, 8, -5])
    VIAGRA = pdb.PDBMolecule('pdb/viagra.pdb', center=False, offset=[3, -3, -7])
    BENZENE = pdb.PDBMolecule('pdb/benzene.pdb', center=False, offset=[0, 8, -5])

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''

    # Rotate the molecules updating its orientation (a persistent modification)
    ETHANOL.rotate([1, 1, 0], RAD_PER_SCENE)
    VIAGRA.rotate([1, 0, 1], RAD_PER_SCENE)
    BENZENE.rotate([0, 1, 1], RAD_PER_SCENE)

    # Return the scene for rendering
    print('@Step: ', step)

    # Combine molecule objects (an object.povray_molecule is a list of atoms, they need
    # to be concatenated to be added to the scene)
    molecules = ETHANOL.povray_molecule + VIAGRA.povray_molecule + BENZENE.povray_molecule

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # light(s) and in this case, molecules too.
    return Scene(povray.default_camera,
                 objects=[povray.default_light, FRONT_LIGHT] + molecules,
                 included=['colors.inc'])

def main(args):
    ''' Runs the simulation '''
    if args.time:
        # Create objects for the scene (i.e. parse PDB files)
        scene_objects()
        # User entered the specific timepoint to render (in seconds)
        povray.make_frame(args.time, scene, time=True)
    else:
        # No output file type and no specific time, exit
        if not args.gif and not args.mp4:
            parser.print_help()
            sys.exit('\nPlease specify either a specific time point or output format for a movie file')
        else:
            # Create objects for the scene (i.e. parse PDB files)
            scene_objects()
        # Render a movie, depending on output type selected (both files is possible)
        if args.gif:
            povray.render_scene_to_gif(scene, args.mp4, time=True)
        if args.mp4:
            povray.render_scene_to_mp4(scene, args.gif, time=True)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Render PDB files using Python and Povray')
    parser.add_argument('--config', default='default.ini')
    parser.add_argument('--time', type=float,
                        help='A specific time (T) in seconds to render (single image output file)')
    parser.add_argument('--gif', action="store_true", default=False,
                        help='Create a GIF movie file using moviepy. Note; this reduces the output quality')
    parser.add_argument('--mp4', action="store_true", default=False,
                        help='Create a high-quality MP4 output file using ffmpeg')

    pargs = parser.parse_args()

    # Read configuration file, either default or the user supplied version
    povray.SETTINGS = load_config(args.config)

    sys.exit(main(pargs))
