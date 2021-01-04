#!/usr/bin/env python3

"""
Code description
"""

__author__ = "Dennis Wiersma & Orfeas Gkourlias"

import sys
from pypovray import pypovray, SETTINGS, models, logger
from vapory import Scene, Camera


def objects():
    """Creates molecules and contains other constants"""


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Scene goes here

    return Scene(Camera('location', [0, 18, -20], 'look_at', [0, 0, 0]),
                 objects=[models.default_light, models.checkered_ground])


def main(args):
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_mp4(frame)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
