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
        1.5 : the radius of the circle falling through the membrane
        1.0 : 'gamma'; the angle of the pinch
        1.5 : the start (y-value) of the circle 'falling through the membrane'
        -5  : the stop (y-value)
        nframes : number of frames for the simulation
        [0, 2, 0] : the offset to move the membrane around the scene
    '''
    nframes = SETTINGS.Duration * SETTINGS.RenderFPS
    coordinates = drop.membrane(step, 1.5, 1.0, 1.5, -5, nframes, [0, 2, 0])
    
    ''' The 'coordinates' is a list containing three-element lists with x- y- and z-coordinates
    that we can use to draw Spheres (this example) or for positioning lipoproteins etc.
    '''
    spheres = []
    for coord in coordinates:
        # Use the coordinates to place a sphere with radius 0.11
        spheres.append(Sphere([coord[0], coord[1], coord[2]], 0.11,
        povray.default_sphere_model))
    
    # The camera looks straight at the membrane otherwise the vesicle looks like an ellipse
    camera = Camera('location', [0, 0, -10], 'look_at', [0, 0, 0])
    return Scene(camera, objects=[povray.default_light] + spheres)

if __name__ == '__main__':
    # Uncomment to use prototype settings
    #povray.SETTINGS = load_config('prototype.ini')
    povray.render_scene_to_gif(scene, time=False)