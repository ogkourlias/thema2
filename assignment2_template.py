#!/usr/bin/env python

from vapory import Cylinder, Cone, Pigment, Texture, Finish

def legend(start_position, axis_length):
    ''' Function docstring '''
    print('Start position:', start_position)
    ## Set the END position to the START + AXIS_LENGTH
    x_cylinder_end = list(start_position)
    y_cylinder_end = list(start_position)
    z_cylinder_end = list(start_position)

    # Add the AXIS_LENGTHs to the corresponding coordinate
    x_cylinder_end[0] += axis_length
    y_cylinder_end[1] += axis_length
    z_cylinder_end[2] += axis_length

    ''' DRAW THE CYLINDERS '''


    # Cone START is the same as the Cylinder END, so we COPY these lists
    x_cone_start = list(x_cylinder_end)
    y_cone_start = list(y_cylinder_end)
    z_cone_start = list(z_cylinder_end)

    # COPY the
    x_cone_end = list(x_cone_start)
    y_cone_end = list(y_cone_start)
    z_cone_end = list(z_cone_start)
    
    # Cone END is the Cylinder END + 1
    x_cone_end[0] += 1
    y_cone_end[1] += 1
    z_cone_end[2] += 1

    ''' DRAW THE CONES '''


    # Add ALL objects to a LIST and return
    legend = [x_cylinder, y_cylinder, z_cylinder, 
              x_cone, y_cone, z_cone]

    return legend

