# !/usr/bin/env python3


"""
This program calls upon fucntions & provides those functions with values to render an animation of rna synthesis.
A lot of the variables are calculated in fractions, so it may function for any duration.
For the best looking results I'd suggest putting a duration of 1/3'd of the sequence character count.
Most test runs were done on a sequence of 60 characters long, over a 20 second duration.
"""

__author__ = "Orfeas Gkourlias & Dennis Wiersma"

from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import *
from dna import sequence, nucleotide, rna_objects, synthesis
from rna_polymerase import rna_polymerase

# TTTTAAAAGCCATAGGAATAGATACCGAAGTTATATCTATAAACAACTGACATTTAATAAATTGTATTCATAGCCTA


def frame(step):  # Main fucntion to render frame.

    nucleotide_final, post_tata_sequence, pre_tata_distance, nucleotide_distance = nucleotide(sequence)
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    # camera
    new_all = Sphere([0, 5.5, 0], 2, models.default_c_model)

    if step < (0.2*nframes):
        camera_distance = pre_tata_distance
        camera_speed = camera_distance / (0.2*nframes)
        cam_x = camera_speed*step
        camera = Camera('location', [cam_x, 40, -80],
                        'look_at', [camera_speed*step, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top,\
        nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance\
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)

    elif step >= (0.2*nframes) and step < (0.4*nframes):
        cam_x = pre_tata_distance
        camera = Camera('location', [cam_x, 40, -80], 'look_at', [cam_x, 0, 0])
        polymerase = rna_polymerase([cam_x, 0, 0], 12)
        transition_top, transition_bot, stretch_bot, stretch_top,\
        nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance\
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)

    elif step >= (0.4*nframes) and step < (0.6*nframes):
        cam_x = pre_tata_distance
        poly_y = (step - 0.4*nframes) * (-15/(0.2*nframes))
        polymerase = rna_polymerase([cam_x, poly_y, 0], 12)
        camera = Camera('location', [cam_x, 40, -80],
                        'look_at', [cam_x, 0, 0])
        stretch_speed = ((step - 159) * (12/80))
        transition_top, transition_bot, stretch_bot, stretch_top,\
        nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance\
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance, stretch_speed)

    else:
        stretch_speed = ((0.2*nframes) * (12/(0.2*nframes)))
        transition_top, transition_bot, stretch_bot, stretch_top,\
        nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance \
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance, stretch_speed)
        post_tata_x = pre_tata_distance + (step - 0.6*nframes) * (post_tata_distance / (nframes*0.4))

        count = int((post_tata_x - pre_tata_distance) // 9)
        new_all = Merge(synthesis(post_tata_sequence, count, new_all, pre_tata_distance), new_all)
        polymerase = rna_polymerase([post_tata_x, -15, 0], 12)
        camera = Camera('location', [post_tata_x, 40, -80], 'look_at', [post_tata_x, 0, 0])
        cam_x = post_tata_x

    return Scene(camera,
                 objects=[LightSource([cam_x, 8, -20], 0.8), polymerase, nucleotide_final, transition_bot,
                          transition_top, stretch_bot, stretch_top, nucleotide_top_stretched,
                          nucleotide_bot_stretched, new_all])


if __name__ == '__main__':

    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
