#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import *

from dna import sequence, nucleotide, pov
from rna_polymerase import rna_polymerase


def frame(step):

    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    return Scene(pov,
                 objects=[models.default_light, polymerase] + nucleotide_final)


if __name__ == '__main__':

    nucleotide_final = nucleotide(sequence)
    polymerase = rna_polymerase([0, 2, 0], 3)

    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
