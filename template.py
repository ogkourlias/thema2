#!/usr/bin/env python3
"""
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building

    usage:
        python3 template.py
"""

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.2"

import sys
from pypovray import pypovray, SETTINGS, models, logger
from vapory.vapory import Sphere, Scene


def scene(step):
    """ Returns the scene at step number (1 step per frame) """
    nframes = SETTINGS.RenderFPS * SETTINGS.Duration

    # Start- and end-points
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
    sphere = Sphere([x_coord, 0, 0], 2, models.default_sphere_model)

    logger.info(" @Step: %s", step)

    # Return the Scene object containing all objects for rendering
    return Scene(models.default_camera,
                 objects=[sphere, models.default_ground, models.default_light])


def main(args):
    """ Main function performing the rendering """
    pypovray.render_scene_to_mp4(scene)

    # (example) render a single PNG image given a step number
    #pypovray.render_scene_to_png(scene, 10)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
