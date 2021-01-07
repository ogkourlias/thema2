#!/usr/bin/env python3
from pypovray import pypovray, models, load_config
import sys
from vapory import Cone, Cylinder, Scene, Text, Camera, Merge

SETTINGS = load_config('default.ini')
sequence = (sys.argv[1])
pov = Camera('location', [0, 20, -80], 'look_at', [0, 2, -5])


def nucleotide(sequence):
    nucleotide_distance = 0
    top = Cylinder([-10, 8, 0], [(len(sequence) * 9), 8, 0], 3, models.default_sphere_model)
    bot = Cylinder([-10, -8, 0], [(len(sequence) * 9), -8, 0], 3, models.default_sphere_model)
    nucleotide1 = Merge(top, bot)
    for letter in sequence:
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


    return [nucleotide1]

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
