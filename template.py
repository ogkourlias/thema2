#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import Scene, Plane, Camera


def objects():
    """Creates molecules and contains other constants"""


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    return Scene(Camera('location', [0, 18, -20], 'look_at', [0, 0, 0]),
                 objects=[models.default_light, models.checkered_ground])


if __name__ == '__main__':
    # Create molecule(s)
    objects()

    # Render as a single image
    pypovray.render_scene_to_png(frame)
