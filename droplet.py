#!/usr/bin/env python3

'''
Demonstrates how extracellular elements can enter a membrane through pinocytosis

Uses a mathematical model devised by Dr. T. Wassenaar
    see povray/drop.py
'''

from povray import povray, drop, load_config, SETTINGS
from vapory import Camera, Scene, Sphere

def scene(step):
    ''' Gets the coordinates of a (variable) number of points on the membrane
    Arguments given to the membrane function are:
        step: the current step (frame number)
        10  : the radius of the circle falling through the membrane
        10  : 'gamma'; the angle of the pinch
        10  : the start (y-value) of the circle 'falling through the membrane'
        -35 : the stop (y-value)
        nframes : number of frames for the simulation
        [0, 2, 0] : the offset to move the membrane around the scene
        80  : the total length (povray 'units') of the membrane
        2.0 : the 'apl' defines the space between the coordinates (with size = 80 and apl = 2.0 you get
              40 coordinates (80/2) for a straight membrane)
    
    When increasing the 'size' and 'apl' parameters remember to also increase the 'radius', 'gamma'
    and 'start/stop' values accordingly.
    '''
    nframes = SETTINGS.Duration * SETTINGS.RenderFPS
    coordinates = drop.membrane(step, 10, 5, 11, -35, nframes, offset=[0, 15, 0], size=80, apl=2.0)

    ''' The 'coordinates' is a list containing three-element lists with x- y- and z-coordinates
    that we can use to draw Spheres (this example) or for positioning lipoproteins etc. '''
    spheres = []
    for coord in coordinates:
        # Use the coordinates to place a sphere with radius 0.11
        spheres.append(Sphere([coord[0], coord[1], coord[2]], 1,
                       povray.default_sphere_model))

    # The camera looks straight at the membrane otherwise the vesicle looks like an ellipse
    camera = Camera('location', [0, 0, -60], 'look_at', [0, 0, 0])
    return Scene(camera, objects=[povray.default_light] + spheres)

if __name__ == '__main__':
    # Uncomment to use prototype settings
    #povray.SETTINGS = load_config('prototype.ini')
    povray.render_scene_to_gif(scene, time=False)
