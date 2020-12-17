#!/usr/bin/env python3
from pypovray import pypovray, models
from vapory import Scene, Camera, Cylinder, Sphere, Merge


def dna_polymerase(position, size, length=0.6):
    x_coord = position[0]
    y_coord = position[1]
    z_coord = position[2]
    length_offset = size * length

    object_left = Sphere([x_coord - length_offset, y_coord, z_coord], size, models.default_sphere_model)
    object_middle = Cylinder([x_coord - length_offset, y_coord, z_coord], [x_coord + length_offset, y_coord, z_coord],
                             size, models.default_sphere_model)
    object_right = Sphere([x_coord + length_offset, y_coord, z_coord], size, models.default_sphere_model)
    merged_object = Merge(object_left, object_middle, object_right)

    return merged_object


def frame(step):
    polymerase = dna_polymerase([0, 2, 0], 3)
    return Scene(Camera('location', [0, 18, -20], 'look_at', [0, 0, 0]),
                 objects=[models.default_light, models.checkered_ground,
                          polymerase])


if __name__ == '__main__':
    # Render as a single image
    pypovray.render_scene_to_png(frame)
