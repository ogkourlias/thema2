#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import Scene, Plane, Camera


def molecules():


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    rotation = (math.pi / 180) * (360 / nframes)
    ATP.rotate([0, 1, 0], rotation)
    phosphate.rotate([0, 1, 0], rotation)
    # Return the Scene object for rendering
    print(rotation)
    return Scene(Camera('location', [0, 18, -20], 'look_at', [0, 0, 0]),
                 objects=[models.default_light,
                          models.checkered_ground] + ATP.povray_molecule + phosphate.povray_molecule)


if __name__ == '__main__':
    # Create molecule(s)
    molecules()

    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
