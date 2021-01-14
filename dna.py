# !/usr/bin/env python3


"""
This program provides function that each contribute to rendering a part of rna synthesis.
Rendering is done with PoVray.
These functions have been written with the intent of being used for an assignment.
The main file that calls upon these functions is movie.py.
"""

__author__ = "Orfeas Gkourlias & Dennis Wiersma"

from pypovray import pypovray, models, load_config
import sys
from vapory import Cone, Cylinder, Scene, Text, Camera, Merge, Sphere

SETTINGS = load_config('default.ini')
sequence_file = open(sys.argv[1])
sequence = ""

for line in sequence_file:
    if ">" not in line:
        line = line.rstrip()
        for letter in line:
            sequence += letter


pov = Camera('location', [0, 20, -200], 'look_at', [0, 2, -5])


# This function creates the first static dna, up until the promoter, where the sequenceh as to be seperated.
def nucleotide(sequence):
    tata_box = "TATAAA"
    sequence_list = sequence.split(tata_box)
    pre_tata = sequence_list[0]
    post_tata = tata_box + sequence_list[1]
    nucleotide_distance = 0
    top = Cylinder([-10, 8, 0],
                   [(len(pre_tata) * 9), 8, 0], 3, models.default_dna_model)
    bot = Cylinder([-10, -8, 0],
                   [(len(pre_tata) * 9), -8, 0], 3, models.default_dna_model)
    pre_tata_distance = (len(pre_tata) * 9)
    nucleotide_row = Merge(top, bot)

    for letter in pre_tata:

        if letter == "C":
            model_top = models.default_c_model
            model_bot = models.default_g_model
        elif letter == "G":
            model_top = models.default_g_model
            model_bot = models.default_c_model
        elif letter == "A":
            model_top = models.default_a_model
            model_bot = models.default_t_model
        elif letter == "T":
            model_top = models.default_t_model
            model_bot = models.default_a_model

        nucleotidetop = Cylinder([nucleotide_distance, 6, 0],
                                 [nucleotide_distance, 0, 0], 3, model_top)
        nucleotidebot = Cylinder([nucleotide_distance, -6, 0],
                                 [nucleotide_distance, 0, 0], 3, model_bot)
        nucleotide_row = Merge(nucleotide_row, nucleotidetop, nucleotidebot)
        nucleotide_distance += 9

    return [nucleotide_row, post_tata, pre_tata_distance, nucleotide_distance]


# This function renders the following sequence with variable coordinates,
# because the sequence will have to expand later.
def rna_objects(post_tata, cam_x, nucleotide_distance, stretch_rate=0):
    stretch_positive = 8
    stretch_negative = -8

    stretch_positive_nucleotide = 6
    stretch_negative_nucleotide = -6
    default_top = 0
    default_bot = 0

    transition_top = Cylinder([cam_x + 20, stretch_positive + stretch_rate, 0],
                              [(len(post_tata) * 9) + cam_x,
                               stretch_positive + stretch_rate,
                               0], 3,
                              models.default_dna_model)
    transition_bot = Cylinder([cam_x + 20, stretch_negative - stretch_rate, 0],
                              [(len(post_tata) * 9) + cam_x,
                               stretch_negative - stretch_rate,
                               0], 3,
                              models.default_dna_model)

    post_tata_distance = len(post_tata) * 9

    stretch_top = Cylinder([cam_x, stretch_positive, 0],
                           [cam_x + 20, stretch_positive + stretch_rate,
                            0], 3,
                           models.default_dna_model)
    stretch_bot = Cylinder([cam_x, stretch_negative, 0],
                           [cam_x + 20, stretch_negative - stretch_rate,
                            0], 3,
                           models.default_dna_model)

    nucleotide_top_stretched = Sphere([0, 5.5, 0], 2, models.default_c_model)
    nucleotide_bot_stretched = Sphere([0, 5.5, 0], 2, models.default_dna_model)

    for letter in post_tata:

        if letter == "C":
            model_top = models.default_c_model
            model_bot = models.default_g_model

        if letter == "G":
            model_top = models.default_g_model
            model_bot = models.default_c_model

        if letter == "A":
            model_top = models.default_a_model
            model_bot = models.default_t_model

        if letter == "T":
            model_top = models.default_t_model
            model_bot = models.default_a_model


        nucleotidetop = Cylinder([nucleotide_distance,
                                  stretch_positive_nucleotide +
                                  stretch_rate, 0],
                                 [nucleotide_distance,
                                  default_top + stretch_rate, 0],
                                 3, model_top)
        nucleotidebot = Cylinder([nucleotide_distance,
                                  stretch_negative_nucleotide -
                                  stretch_rate, 0],
                                 [nucleotide_distance,
                                  default_bot - stretch_rate, 0], 3,
                                 model_bot)



        nucleotide_top_stretched = Merge(nucleotide_top_stretched,
                                         nucleotidetop)
        nucleotide_bot_stretched = Merge(nucleotide_bot_stretched,
                                         nucleotidebot)

        nucleotide_distance += 9
    return [transition_top, transition_bot, stretch_top, stretch_bot, nucleotide_top_stretched,
            nucleotide_bot_stretched, post_tata_distance]


# Renders the RNA Molecule, depending on the post promoter length. Also includes a new colour for uracil.
def synthesis(post_tata, count, new_all, pre_tata_distance):
    for number in range(count + 1):
        x_all = pre_tata_distance + number * 9
        if number > 5:
            if post_tata[number] == "C":
                model = models.default_c_model
            elif post_tata[number] == "G":
                model = models.default_g_model
            elif post_tata[number] == "A":
                model = models.default_a_model
            elif post_tata[number] == "T":
                model = models.default_u_model
            new_top_roof = Cylinder([x_all - 5, -6, 0], [x_all + 5, -6, 0], 3, models.default_dna_model)
            new_top = Cylinder([x_all, -6, 0], [x_all, -12, 0], 3, model)
            new_all = Merge(new_top, new_all, new_top_roof)

    return new_all


def frame(step):
    return Scene(pov,
                 objects=[models.default_light])


if __name__ == '__main__':
    # Render as an image
    pypovray.render_scene_to_png(frame)
