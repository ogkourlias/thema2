#!/usr/bin/env python3
"""
Renders a movie using Povray

To install the requirements (moviepy, ffmpy and vapory), use:
    pip install -r requirements.txt
"""

import argparse
import sys
from pypovray import pypovray, SETTINGS, load_config
from vapory import Scene, LightSource, Camera, Sphere, Cylinder, Plane, Texture, Pigment, Finish, Interior, Difference

# Scene Global Settings
RADIUS = 10  # scene circle radius

# Scene Settings and Static Objects
MAIN_LIGHT = LightSource([2, 4, -3], 3, 'fade_distance', 5,
                         'fade_power', 2, 'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
BACK_LIGHT = LightSource([-8, 3, -1], 'color', [1, 0.8, 0, 4],
                         'fade_distance', 6, 'fade_power', 2,
                         'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
CAMERA = Camera('location', [0, 10, -20], 'look_at', [0, 0, -3])
GROUND = Plane([0, 1, 0], -4, Texture(Pigment('color', [1.5, 1, 1])))

def sphere_circle():
    """ Creates a circle made up of 20 small spheres.
        A list of Sphere objects is returnded ready for rendering. """
    spheres = 20  # number of spheres to create
    ring = []
    ring_node_size = 0.6
    smodel = Texture(Pigment('color', [1, 0, 0], 'filter', 0.5),
                     Finish('phong', 0.8, 'reflection', 0.5))
    for i in range(spheres):
        ring.append(Sphere([0, 0, 0], ring_node_size, smodel,
                           'translate', [RADIUS, 0, 0],
                           'rotate', [0, 360/spheres * i, 0]))
    return ring


# Create a list of sphere objects forming the circle (only build once)
RING = sphere_circle()


def frame(step):
    """ Returns the scene at the given step  """
    ## Rotating sphere
    sphere_rad = 1.8
    sphere = Sphere([0, 0, 0], sphere_rad,
                    Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
                    Interior('ior', 1), Finish('phong', 0.6, 'reflection', 0.4))

    # Intersecting cylinder object
    rod = Cylinder([0, 0, 3], [0, 0, -3],
                   1.0, 'open', Pigment('color', [1, 0, 0], 'filter', 0.8),
                   Interior('ior', 1), Finish('phong', 0, 'reflection', 0))

    # 'Hollow out' the rotating sphere with the intersecting cylinder using the Difference,
    # move to a spot on the circle (top) and rotate on the x-axis
    traveller = Difference(sphere, rod, 'translate', [0, RADIUS, 0],
                           'rotate', [0, 360/eval(SETTINGS.NumberFrames)*step*2, 0])

    return Scene(CAMERA, objects=[GROUND, MAIN_LIGHT, BACK_LIGHT, traveller] + RING)


def main(args):
    """ Runs the simulation """
    if args.time:
        # User entered the specific timepoint to render (in seconds)
        pypovray.render_scene_to_png(frame, args.time)
    else:
        # No output file type and no specific time, exit
        if not args.gif and not args.mp4:
            parser.print_help()
            sys.exit('\nPlease specify either a specific time point or output format for a movie file')
        # Render a movie, depending on output type selected (both files is possible)
        if args.gif:
            pypovray.render_scene_to_gif(frame)
        if args.mp4:
            pypovray.render_scene_to_mp4(frame)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a rendered movie using Povray')
    parser.add_argument('--time', type=float,
                        help='A specific time (T) in seconds to render (single image output file)')
    parser.add_argument('--gif', action="store_true", default=False,
                        help='Create a GIF movie file using moviepy. Note; this reduces the output quality')
    parser.add_argument('--mp4', action="store_true", default=False,
                        help='Create a high-quality MP4 output file using ffmpeg')

    args = parser.parse_args()
    sys.exit(main(args))
