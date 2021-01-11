#!/usr/bin/env python3
from pypovray import pypovray, models, load_config
import sys
from vapory import Cone, Cylinder, Scene, Text, Camera, Merge, Sphere

SETTINGS = load_config('default.ini')
sequence = (sys.argv[1])
pov = Camera('location', [0, 20, -200], 'look_at', [0, 2, -5])


def nucleotide(sequence):
    tata_box = "TATAAA"
    sequence_list = sequence.split(tata_box)
    pre_tata = sequence_list[0]
    post_tata = tata_box + sequence_list[1]
    nucleotide_distance = 0
    top = Cylinder([-10, 8, 0], [(len(pre_tata) * 9), 8, 0], 3, models.default_dna_model)
    bot = Cylinder([-10, -8, 0], [(len(pre_tata) * 9), -8, 0], 3, models.default_dna_model)
    pre_tata_distance = (len(pre_tata)*9)
    nucleotide1 = Merge(top, bot)

    for letter in pre_tata:

        if letter == "C":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)

        elif letter == "G":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)

        elif letter == "A":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)

        elif letter == "T":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)


        nucleotide_distance += 9

    return [nucleotide1, post_tata, pre_tata_distance, nucleotide_distance]

def rna_objects(post_tata, cam_x, nucleotide_distance, stretch_rate = 0):
    stretch_positive = 8
    stretch_negative = -8

    stretch_positive_nucleotide = 6
    stretch_negative_nucleotide = -6
    default_top = 0
    default_bot = 0

    transition_top = Cylinder([cam_x + 20, stretch_positive + stretch_rate, 0], [(len(post_tata) * 9)+cam_x , stretch_positive + stretch_rate, 0], 3, models.default_dna_model)
    transition_bot = Cylinder([cam_x + 20, stretch_negative - stretch_rate, 0], [(len(post_tata) * 9)+cam_x , stretch_negative - stretch_rate, 0], 3, models.default_dna_model)

    post_tata_distance = len(post_tata) * 9

    stretch_top = Cylinder([cam_x, stretch_positive, 0], [cam_x + 20, stretch_positive + stretch_rate, 0], 3, models.default_dna_model)
    stretch_bot = Cylinder([cam_x, stretch_negative, 0], [cam_x + 20, stretch_negative - stretch_rate, 0], 3, models.default_t_model)

    nucleotide_top_stretched = Sphere([2, 5.5, -2], 2, models.default_c_model)
    nucleotide_bot_stretched = Sphere([2, 5.5, -2], 2, models.default_dna_model)

    for letter in post_tata:

        if letter == "C":
            nucleotidetop = Cylinder([nucleotide_distance, stretch_positive_nucleotide + stretch_rate, 0], [nucleotide_distance, default_top + stretch_rate, 0], 3, models.default_c_model)
            nucleotidebot = Cylinder([nucleotide_distance, stretch_negative_nucleotide - stretch_rate, 0], [nucleotide_distance, default_bot - stretch_rate, 0], 3, models.default_g_model)
            nucleotide_top_stretched = Merge(nucleotide_top_stretched, nucleotidetop)
            nucleotide_bot_stretched = Merge(nucleotide_bot_stretched, nucleotidebot)
        if letter == "G":
            nucleotidetop = Cylinder([nucleotide_distance, stretch_positive_nucleotide + stretch_rate, 0], [nucleotide_distance, default_top + stretch_rate, 0], 3, models.default_g_model)
            nucleotidebot = Cylinder([nucleotide_distance, stretch_negative_nucleotide - stretch_rate, 0], [nucleotide_distance, default_bot - stretch_rate, 0], 3, models.default_c_model)
            nucleotide_top_stretched = Merge(nucleotide_top_stretched, nucleotidetop)
            nucleotide_bot_stretched = Merge(nucleotide_bot_stretched, nucleotidebot)
        if letter == "A":
            nucleotidetop = Cylinder([nucleotide_distance, stretch_positive_nucleotide + stretch_rate, 0], [nucleotide_distance, default_top + stretch_rate, 0], 3, models.default_a_model)
            nucleotidebot = Cylinder([nucleotide_distance, stretch_negative_nucleotide - stretch_rate, 0], [nucleotide_distance, default_bot - stretch_rate, 0], 3, models.default_t_model)
            nucleotide_top_stretched = Merge(nucleotide_top_stretched, nucleotidetop)
            nucleotide_bot_stretched = Merge(nucleotide_bot_stretched, nucleotidebot)
        if letter == "T":
            nucleotidetop = Cylinder([nucleotide_distance, stretch_positive_nucleotide + stretch_rate, 0], [nucleotide_distance, default_top + stretch_rate, 0], 3, models.default_t_model)
            nucleotidebot = Cylinder([nucleotide_distance, stretch_negative_nucleotide - stretch_rate, 0], [nucleotide_distance, default_bot - stretch_rate, 0], 3, models.default_a_model)
            nucleotide_top_stretched = Merge(nucleotide_top_stretched, nucleotidetop)
            nucleotide_bot_stretched = Merge(nucleotide_bot_stretched, nucleotidebot)

        nucleotide_distance += 9
    return [transition_top, transition_bot, stretch_top, stretch_bot, nucleotide_top_stretched, nucleotide_bot_stretched, post_tata_distance]

def synthesis(post_tata, cam_x, nucleotide_distance):

    return []



def frame(step):
    # Return the Scene object for rendering
    # top = Cylinder([-10, 8, 0], [(len(sequence) * 9), 8, 0], 3, models.default_sphere_model)
    # bot = Cylinder([-10, -8, 0], [(len(sequence) * 9), -8, 0], 3, models.default_sphere_model)

    nucleotide_final = nucleotide(sequence)

    return Scene(pov,
                 objects=[models.default_light] + nucleotide_final)
if __name__ == '__main__':
    # Render as an image
    pypovray.render_scene_to_png(frame)
    print(sys.argv[1])
    print(len(sequence))
    print()
