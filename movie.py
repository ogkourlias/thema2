#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import *

from dna import sequence, nucleotide, pov, rna_synthesis
from rna_polymerase import rna_polymerase

# Test sequence for now: ACTGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTTCGAGCTAGCTGATCGATCGATCGGGCTATATAAAGCT

def frame(step):

    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    print(rna_sequence)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    # camera
    camera_distance = 400
    camera_speed = camera_distance / 80
    print(step)
    camera = Camera('location', [camera_speed*step, 40, -80], 'look_at', [camera_speed*step, 0, 0])
    polymerase = rna_polymerase([camera_speed*step, 0, 0], 12)

    return Scene(camera,
                 objects=[models.default_light, polymerase, nucleotide_final])


if __name__ == '__main__':

    nucleotide_final, rna_sequence = nucleotide(sequence)
    rna_string = rna_synthesis(sequence)
    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
