from vapory import *

## Input/ output location
file_dir       = '/Users/marcelk/Dropbox/Hanze/Thema02/povray'
## Output movie prefix
outfile_prefix = 'simulation'
imagefile_dir  = 'images'

#########################POVRAY#######################
## Output settings
iwidth                      = 1024
iheight                     = 768
quality                     = 7                             # Povray quality setting ((min) 0-10 (max))
antialias                   = 0.01                          # Povray anti-aliasing (lower is better quality)
duration                    = 6                             # total runtime of the animation
## Render Settings
sfps                        = 10                            # rendered scene frames per second
ftime                       = duration/(duration*sfps)      # time per frame in seconds

## Static Object and Model Library
default_light        = LightSource([2, 4, -3], 1.5)
default_camera       = Camera('location', [0, 14, -28], 'look_at', [0, 0, -3])
default_ground       = Plane([0, 1, 0], -6, Texture(Pigment('color', [1.5, 1, 1])))
default_sphere_model = Texture(Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
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
