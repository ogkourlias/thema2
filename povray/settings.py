from vapory import *

## Input/ output location
file_dir       = '/Users/marcelk/Dropbox/Hanze/Thema02/povray'
## Output movie prefix
outfile_prefix = 'simulation'
imagefile_dir  = 'images'

#########################POVRAY#######################
## Output settings
iwidth                      = 480
iheight                     = 320
quality                     = 6
antialias                   = 0.1
duration                    = 6                             # total time for the animation
## Render Settings
sfps                        = 15                            # rendered scene frames per second
ftime                       = duration/(duration*sfps)      # time per frame  in seconds

## Static Object and Model Library
default_light        = LightSource([2, 4, -3], 1)
default_camera       = Camera('location', [0, 10, -20], 'look_at', [0, 0, -3])
default_ground       = Plane([0, 1, 0], -4, Texture(Pigment('color', [1.5, 1, 1])))
default_sphere_model = Texture(Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
                               Finish('phong', 0.6, 'reflection', 0.4))