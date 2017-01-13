#!/usr/bin/env python3

from povray import povray
from vapory import Sphere, Scene, Pigment, POVRayElement, Cylinder, Camera, Background
from assignment2 import legend
import numpy as np

def scene(step):
    back = Background([1, 1, 1])
    color = np.array([0.7, 1, 0]) * 0.8

    # Storing the cylinders
    cylinders = []
    n = 7
    for i in range(n):
        cylinders.append(Cylinder([0, 0, 0], [1, 0, 0], 1.0, 1.0,
                         'scale', [1, 0.25, 1],
                         'rotate', [-30, 0, 0],
                         'translate', [1.25, 0, 0],
                         'rotate', [0, i * 360/n, 0],
                         Pigment('color', color)))

    prop = Blob('threshold', 0.65,
                Sphere([0, 0, 0], 1.00, 1.00, 'scale', [1, 2, 1], Pigment('color', color)),
                # unpack cylinders
                *cylinders,
                'scale', 1.5,
                'rotate', [0, 0, 0],
                'translate', [0, 0.5, 0]
                )

    camera = Camera('location', [5, 5, -8], 'look_at', [0, 0, 0])
    xyz_legend = legend([-10, 0, 0], 3)
    return Scene(camera, objects=[povray.default_light, prop, back] + xyz_legend)

class Blob(POVRayElement):
    """ Blob(blob_item1, blob_item2, ...) """

if __name__ == '__main__':
    # Render as an image
    povray.make_frame(0, scene, time=True)


