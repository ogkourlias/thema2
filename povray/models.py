from vapory import *

## Static Object and Model Library
default_light        = LightSource([2, 4, -3], 2.5)
default_sphere_model = Texture(Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
                               Finish('phong', 0.6, 'reflection', 0.4))
default_camera       = Camera('location', [0, 14, -28], 'look_at', [0, 0, -3])
default_ground       = Plane([0, 1, 0], -6, Texture(Pigment('color', [1.5, 1, 1])))
floor_camera         = Camera('location', [0, 5, -22], 'look_at', [0, 2, -3])
checkered_ground     = Plane([0, 1, 0], -1,
                             Texture(Pigment('checker',
                             'color', [1, 1, 1], 
                             'color', [0.5,0.5,0.5],
                             'scale', 5)))
text_model           = Texture(Pigment('color', 'Gold'),
                               Finish('phong', 0.6, 'reflection', 0.4))
## Static atom definitions
## See the 'color.inc' povray file for more color examples and names.
atom_colors = {
    'C': [0.4, 0.4, 0.4],
    'H': [1, 1, 1],
    'N': [0, 0, 1],
    'O': [1, 0, 0],
    'P': [1, 0.5, 0],
    'S': [0.6, 0.8, 0.2],
    'OH': [1, 0, 0],
    'HH': [1, 1, 1]
}

atom_sizes = {
    'C': 1,
    'H': 0.65,
    'HH': 0.65,
    'N': 0.9,
    'O': 1,
    'S': 1.2,
    'OH': 1,
    'P': 1.25
}
