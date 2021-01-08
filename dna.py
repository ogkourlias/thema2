#!/usr/bin/env python3
from pypovray import pypovray, models, load_config
import sys
from vapory import Cone, Cylinder, Scene, Text, Camera, Merge

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
    nucleotide1 = Merge(top, bot)
    rna_sequence = ""

    for letter in pre_tata:
        if letter == "C":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)
            rna_sequence += letter

        elif letter == "G":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)
            rna_sequence += letter

        elif letter == "A":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)
            rna_sequence += letter

        elif letter == "T":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
            nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)
            nucleotide1 = Merge(nucleotide1, nucleotidetop, nucleotidebot)
            rna_sequence += "U"

        print(pre_tata , "followed by", post_tata)
        nucleotide_distance += 9


    return [nucleotide1, rna_sequence]

def rna_synthesis(sequence):
    nucleotide_distance = 0
    top = Cylinder([-10, 8, 0], [(len(sequence) * 9), 8, 0], 3, models.default_dna_model)
    rna_string = top
    for letter in sequence:
        if letter == "C":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            rna_string = Merge(top, nucleotidetop)
        elif letter == "G":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            rna_string = Merge(top, nucleotidetop)
        elif letter == "A":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            rna_string = Merge(top, nucleotidetop)
        elif letter == "U":
            nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
            rna_string = Merge(top, nucleotidetop)
        nucleotide_distance += 9

    return [rna_string]

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
