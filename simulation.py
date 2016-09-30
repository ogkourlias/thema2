'''
Renders a movie using Povray

To install the requirements (moviepy, ffmpy and vapory), use:
    pip install -r requirements.txt
'''

from math import sin, cos, pi, sqrt, pow
from vapory import *
from povray import povray
import argparse
import sys

## Scene Global Settings
radius    = 10     # scene circle radius
xcenter   = 0
zcenter   = 0
steps     = 200    # number of steps in a circle
## Scene Settings and Static Objects
main_light = LightSource([2, 4, -3], 3,  'fade_distance', 5,
                         'fade_power', 2, 'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
back_light = LightSource([-8, 3, -1], 'color', [1, 0.8, 0,4],
                         'fade_distance', 6, 'fade_power', 2,
                         'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
camera     = Camera('location', [0, 10, -20], 'look_at', [0, 0, -3])
ground     = Plane([0, 1, 0], -4, Texture(Pigment('color', [1.5, 1, 1])))

def _get_xz(step, steps):
    '''
    Calculates the x- and z-positions given the position in a circle.
    '''
    x = xcenter - sin(float(step) / steps * 2.0 * pi) * radius
    z = zcenter - cos(float(step) / steps * 2.0 * pi) * radius    
    return (x,z)

def sphere_circle():
    spheres = 20 # number of spheres to create
    ring = []
    ring_node_size = 0.6
    smodel = Texture(Pigment('color', [1, 0, 0], 'filter', 0.5), 
                     Finish('phong', 0.8, 'reflection', 0.5))
    for i in range(steps):
        if i % int(steps / spheres)  == 0: # At every 1/8th place a sphere
            x, z = _get_xz(i, steps)
            ring.append(Sphere([x, 0, z], ring_node_size, smodel))
    return ring

# Create a list of sphere objects forming the circle (only build once)
ring = sphere_circle()

def scene(t):
    """ Returns the scene at time 't' (in seconds) """
    x, z = _get_xz(t, steps)

    ## Rotating sphere
    sphere_rad = 1.8
    sphere_diam = sphere_rad * 2
    sphere = Sphere([x, 0, z], sphere_rad,
                    Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
                    Interior('ior',1), Finish('phong', 0.6, 'reflection', 0.4))

    ## Intersecting cylinder
    t_slope  = 0 if x == 0 else (zcenter - z) / (xcenter - x) 
    inv_slope = 0 if t_slope == 0 else -(1 / t_slope)

    # Calculate x and y of cylinder end-points given length of side c (right triangle)
    c = sphere_rad
    # Length of sides a and b of the triangle
    # See: http://math.stackexchange.com/questions/566029/in-a-right-triangle-given-
    #      slope-and-length-of-hypotenuse-find-length-of-legs
    b = c / sqrt(inv_slope**2 + 1)
    a = sqrt(abs(c**2 - b**2))

    # Coordinates extending to the right of the 'spoke' end
    r_x_end = x + b if z >= 0 else x - b
    r_z_end = z - a if x >= 0 else z + a

    # Coordinates extending to the left of the 'spoke' end
    l_x_end = x - b if z >= 0 else x + b
    l_z_end = z + a if x >= 0 else z - a

    # Intersecting cylinder object
    rod = Cylinder([l_x_end, 0, l_z_end], [r_x_end, 0, r_z_end],
                   1.0, 'open', Pigment('color', [1, 0, 0], 'filter', 0.8),
                   Interior('ior',1), Finish('phong', 0, 'reflection', 0))

    return Scene(camera,
                 objects=[ground, main_light, back_light, Difference(sphere, rod)] + ring,
                 included=["glass.inc", "colors.inc", "textures.inc"])

if __name__ == 'vapory':
    parser = argparse.ArgumentParser(description='Create a rendered movie using Povray')
    parser.add_argument('--time', type=float, 
                        help='A specific time (T) in seconds to render (single image output file)')
    parser.add_argument('--gif', action="store_true", default=False,
                        help='Create a GIF movie file using moviepy. Note; this reduces the output quality')
    parser.add_argument('--mp4', action="store_true", default=False,
                        help='Create a high-quality MP4 output file using ffmpeg')

    args = parser.parse_args()

    if args.time:
        # User entered the specific timepoint to render (in seconds)
        povray.make_frame(args.time, scene)
    else:
        # No output file type and no specific time, exit
        if not args.gif and not args.mp4:
            parser.print_help()
            sys.exit('\nPlease specify either a specific time point or output format for a movie file')
        # Render a movie, depending on output type selected (both files is possible)
        if args.gif:
            povray.render_scene_gif(scene, args.mp4)
        if args.mp4:
            povray.render_scene_to_mp4(scene, args.gif)