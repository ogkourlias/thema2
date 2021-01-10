#!/usr/bin/env python3
import math
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import *

from dna import sequence, nucleotide, rna_objects
from rna_polymerase import rna_polymerase

# Test sequence for now: TTTTAAAAGCCATAGGAATAGATACCGAAGTTATATCTATAAACAACTGACATTTAATAAATTGTATTCATAGCCTAATGTGATGAGCCACAGAAGCTTGCAAACTTTAATG

def frame(step):

    nucleotide_final, rna_sequence, pre_tata_distance, nucleotide_distance = nucleotide(sequence)

    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    print(rna_sequence)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    # camera

    print(step)

    if step < 80:
        camera_distance = pre_tata_distance
        camera_speed = camera_distance / 80
        cam_x = camera_speed*step
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [camera_speed*step, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched = rna_objects(rna_sequence, pre_tata_distance, nucleotide_distance)
    elif step >= 80 and step < 160:
        cam_x = pre_tata_distance
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [cam_x, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched = rna_objects(rna_sequence, pre_tata_distance, nucleotide_distance)
    else: #elif step >= 160 and step < 240:
        cam_x = pre_tata_distance
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [cam_x, 0, 0])
        stretch_speed = ((step - 159) * (12/4))
        print(stretch_speed)
        transition_top, transition_bot, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched = rna_objects(rna_sequence, pre_tata_distance, nucleotide_distance, stretch_speed)


    # transition_top, transition_bot, stretch_bot, stretch_top = rna_objects(rna_sequence, pre_tata_distance)

    return Scene(camera,
                 objects=[models.default_light, polymerase, nucleotide_final, transition_bot, transition_top, stretch_bot, stretch_top, nucleotide_top_stretched, nucleotide_bot_stretched])


if __name__ == '__main__':

    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
