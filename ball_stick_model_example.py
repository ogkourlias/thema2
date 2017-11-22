#!/usr/bin/env python3

"""
Example of the ball-and-stick model for rendering a molecule from a PDB file.
"""

# IMPORTS
from pypovray import pypovray, SETTINGS, pdb, models
from vapory.vapory import Scene
from math import pi
import sys


# METADATA
__author__  = 'Niels van der Vegt'
__status__  = 'Example'
__version__ = 'e.v1'


# FUNCTIONS
def create_viagra_molecule():
    """
    Creates and places a molecule for rendering based on VIAGRA's PDB file.
    """
    global VIAGRA
    # Declare pypovray molecule from PDB file.
    VIAGRA = pdb.PDBMolecule('{}/pdb/viagra.pdb'.format(SETTINGS.AppLocation), center=True)
    VIAGRA.move_offset([0, 1, 0])

def scene(step):
    """
    Renders an animation of a VIAGRA molecule. It's atoms expand, making space
    for the ball-stick model to initialize. This gives an overview of the atoms
    within this molecule halfway through the animation, before returning to its
    original radii.
    """
    # Declare the amount of rotation to be performed each step of the animation.
    rotate_coordinates = pi * 2 / 180
    VIAGRA.rotate([0, 1, 0], rotate_coordinates)

    # Steps to complete in the first half of the animation.
    if step < 105:
        # Increase the distance between the molecule's atoms.
        # The revert parameter means scale factors do not stack. This is useful
        # as we'll be using step to increment our scale factor.
        VIAGRA.scale_atom_distance(1 + (step / 105), revert = True)
    elif step > 105:
        # Decrease the distance between the molecule's atoms.
        VIAGRA.scale_atom_distance(2 - ((step - 105) / 105), revert = True)

    # Render the ball-stick model.
    VIAGRA.show_stick_model(stick_radius = 0.4)

    return Scene(models.default_camera,
                 objects=[models.default_light] + VIAGRA.povray_molecule)


def main():
    """
    Runs all functionalities of the script.
    """
    create_viagra_molecule()
    pypovray.render_scene_to_mp4(scene)


# ENTRYPOINT
if __name__ == "__main__":
    sys.exit(main())

