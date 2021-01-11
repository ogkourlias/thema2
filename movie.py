#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import *

from dna import sequence, nucleotide, rna_objects
from rna_polymerase import rna_polymerase

# Test sequence for now: TTTTAAAAGCCATAGGAATAGATACCGAAGTTATATCTATAAACAACTGACATTTAATAAATTGTATTCATAGCCTAATGTGATGAGCCACAGAAGCTTGCAAACTTTAATG

def frame(step):

    nucleotide_final, post_tata_sequence, pre_tata_distance, nucleotide_distance = nucleotide(sequence)

    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    # camera

    print(step)

    if step < (0.2*nframes):
        camera_distance = pre_tata_distance
        camera_speed = camera_distance / 80
        cam_x = camera_speed*step
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [camera_speed*step, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)
    elif step >= (0.2*nframes) and step < (0.4*nframes):
        cam_x = pre_tata_distance
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [cam_x, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)
    elif step >= (0.4*nframes) and step < (0.6*nframes):
        cam_x = pre_tata_distance
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [cam_x, 0, 0])
        stretch_speed = ((step - 159) * (12/80))
        print(stretch_speed)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance, stretch_speed)
    else:
        stretch_speed = (80 * (12/80))
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance, stretch_speed)
        post_tata_x = pre_tata_distance + (step - 0.6*nframes) * (post_tata_distance / (nframes*0.4))
        polymerase = rna_polymerase([post_tata_x, 0, 0], 12)
        camera = Camera('location', [post_tata_x, 40, -80], 'look_at', [post_tata_x, 0, 0])
        print(stretch_speed)



    return Scene(camera,
                 objects=[models.default_light, polymerase, nucleotide_final, transition_bot, transition_top, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched])


if __name__ == '__main__':

    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
