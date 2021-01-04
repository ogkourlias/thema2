#!/usr/bin/env python3
from pypovray import pypovray, models, load_config
import sys
from vapory import Cone, Cylinder, Scene, Text, Camera

SETTINGS = load_config('default.ini')
sequence = (sys.argv[1])
pov = Camera('location', [0, 20, -80], 'look_at', [0, 2, -5])

def nucleotide(letter, nucleotide_distance):
    if letter == "C":
        nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
        nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
    elif letter == "G":
        nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_g_model)
        nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_c_model)
    elif letter == "A":
        nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)
        nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
    elif letter == "T":
        nucleotidetop = Cylinder([nucleotide_distance, 6, 0], [nucleotide_distance, 0, 0], 3, models.default_t_model)
        nucleotidebot = Cylinder([nucleotide_distance, -6, 0], [nucleotide_distance, 0, 0], 3, models.default_a_model)

    return [nucleotidetop, nucleotidebot]

def frame(step):
    nucleotide1 = []
    nucleotide_distance = 0
    for letter in sequence:
        nucleotide1.append(nucleotide(letter, nucleotide_distance))
        nucleotide_distance += 9

    top = Cylinder([-10, 8, 0], [(len(sequence) * 9), 8, 0], 3, models.default_sphere_model)
    bot = Cylinder([-10, -8, 0], [(len(sequence) * 9), -8, 0], 3, models.default_sphere_model)

    nucleotide_final = nucleotide1[0]
    for item in nucleotide1:
        nucleotide_final += item
    # Return the Scene object for rendering
    return Scene(pov,
                 objects=[models.default_light, top, bot] + nucleotide_final)


if __name__ == '__main__':
    # Render as an image
    pypovray.render_scene_to_png(frame)
    print(sys.argv[1])
    print(len(sequence))
