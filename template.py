'''
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2016.1"

import sys
from povray import povray, SETTINGS
from vapory import Sphere, Scene

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    nframes = SETTINGS.RenderFPS * SETTINGS.Duration

    # Starting- and end-point (left side)
    x_start = -10
    x_end = 10
    distance = x_end - x_start
    
    # Calculate distance to move at each step
    distance_per_frame = (distance / nframes) * 2

    # Calculate new x-coordinate
    if step < (nframes / 2):
        # Move from left to right (starting at x = -10)
        x_coord = x_start + step * distance_per_frame
    else:
        # Move from right to left (starting at x = 10)
        x_coord = x_end - (step - (nframes / 2)) * distance_per_frame

    # Create sphere at calculated x-coordinate using default model
    sphere = Sphere([x_coord, 0, 0], 2, povray.default_sphere_model)

    # Return the Scene object for rendering
    return Scene(povray.default_camera,
                 objects=[sphere, povray.default_ground, povray.default_light])

def main(args):
    ''' Main function performing the rendering '''
    # Render as an MP4 movie
    povray.render_scene_to_mp4(scene, time=False)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
