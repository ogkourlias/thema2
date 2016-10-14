'''
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__  = "Marcel Kempenaar"
__status__  = "Template"
__version__ = "2016.1"

from povray import povray, SETTINGS
from vapory import Sphere, Scene

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    print('@ step ', step)
    frames = SETTINGS.RenderFPS * SETTINGS.Duration

    # Calculate distance to move at each step
    distance_per_frame = (20 / frames) * 2

    # Calculate new x-coordinate
    if step < (frames / 2):
        # Move from left to right (starting at x = -10)
        x_coord = -10 + step * distance_per_frame
    else:
        # Move from right to left (starting at x = 10)
        x_coord = 10 - (step - (frames / 2)) * distance_per_frame

    # Create sphere at calculated x-coordinate using default model
    sphere = Sphere([x_coord, 0, 0], 2, povray.default_sphere_model)

    # Return the Scene object for rendering
    return Scene(povray.default_camera,
                 objects=[sphere, povray.default_ground, povray.default_light])

if __name__ == '__main__':
    # Render as an MP4 movie
    povray.render_scene_to_mp4(scene, time=True)
