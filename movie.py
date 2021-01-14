# !/usr/bin/env python3


"""
This program calls upon fucntions
& provides those functions with values to render an animation of rna synthesis.
A lot of the variables are calculated in fractions, so it may function for any duration.
For the best looking results,
I'd suggest putting a duration of 1/3'd of the sequence character count.
Most test runs were done on a sequence of 60 characters long, over a 20 second duration.
"""

__author__ = "Orfeas Gkourlias & Dennis Wiersma"

import sys
from pypovray import pypovray, SETTINGS, models, logger
from vapory import Scene, Camera, Merge, Sphere, LightSource
from dna import nucleotide, rna_objects, synthesis
from rna_polymerase import rna_polymerase


sequence_file = open(sys.argv[1])
sequence_string = ""

for line in sequence_file:
    if ">" not in line:
        line = line.rstrip()
        for letter in line:
            sequence_string += letter

def frame(step):
    """" Main function that renders a frame.
    Calls upon multiple other functions and imported objects."""
    nucleotide_final, post_tata_sequence, \
        pre_tata_distance, nucleotide_distance = nucleotide(sequence_string)
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)
    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)
    # Placeholder sphere (Can't create empty objects)
    new_all = Sphere([0, 5.5, 0], 2, models.default_c_model)

    if step < (0.2 * nframes):
        light_x = pre_tata_distance / (0.2 * nframes) * step
        camera = Camera('location', [pre_tata_distance / (0.2 * nframes) * step, 40, -80],
                        'look_at', [pre_tata_distance / (0.2 * nframes) * step, 0, 0])
        polymerase = rna_polymerase([pre_tata_distance / (0.2 * nframes) * step, 0, 0], 12)

        transition_top, transition_bot, stretch_bot, stretch_top, \
            nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance \
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)

    elif step >= (0.2 * nframes) and step < (0.4 * nframes):
        light_x = pre_tata_distance
        camera = Camera('location', [pre_tata_distance, 40, -80],
                        'look_at', [pre_tata_distance, 0, 0])
        polymerase = rna_polymerase([pre_tata_distance, 0, 0], 12)

        transition_top, transition_bot, stretch_bot, stretch_top, \
            nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance \
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance)

    elif step >= (0.4 * nframes) and step < (0.6 * nframes):
        light_x = pre_tata_distance
        polymerase = rna_polymerase([pre_tata_distance,
                                     (step - 0.4 * nframes) * (-15 / (0.2 * nframes)), 0], 12)
        camera = Camera('location', [pre_tata_distance, 40, -80],
                        'look_at', [pre_tata_distance, 0, 0])

        transition_top, transition_bot, stretch_bot, stretch_top, \
            nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance \
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance,
                          (step - 0.4 * nframes) * (12 / (0.2 * nframes)))

    else:
        transition_top, transition_bot, stretch_bot, stretch_top, \
            nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance \
            = rna_objects(post_tata_sequence, pre_tata_distance, nucleotide_distance,
                          (0.2 * nframes) * (12 / (0.2 * nframes)))
        post_tata_x = pre_tata_distance + (step - 0.6 * nframes) * \
                      (post_tata_distance / (nframes * 0.4))
        new_all = Merge(synthesis(post_tata_sequence, int((post_tata_x - pre_tata_distance) // 9),
                                  new_all, pre_tata_distance), new_all)
        polymerase = rna_polymerase([post_tata_x, -15, 0], 12)
        camera = Camera('location', [post_tata_x, 40, -80], 'look_at', [post_tata_x, 0, 0])
        light_x = post_tata_x

    return Scene(camera,
                 objects=[LightSource([light_x, 8, -20], 0.8), polymerase, nucleotide_final,
                          transition_bot, transition_top, stretch_bot,
                          stretch_top, nucleotide_top_stretched,
                          nucleotide_bot_stretched, new_all])


if __name__ == '__main__':
    # Render as a single image
    pypovray.render_scene_to_mp4(frame)
