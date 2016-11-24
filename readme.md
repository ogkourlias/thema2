# A template project demonstrating the use of the Povray raytracer

## Manuals and Assignments

* ###[Installing and Configuring](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/install_and_configure.ipynb) \[[mirror](https://bioinf.nl/~marcelk/pypovray/install_and_configure.html)\]

    **Guide for Installing and Configuring the software**  
      
    This short document describes how to get the required software (mainly, this Python package), configure it and run one of the included examples on the Bioinformatics computer network. At the bottom of the document is a section on how to do this on your own computer.

* ###[Basic usage of PyPovray](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/povray_basic.ipynb) \[[mirror](https://bioinf.nl/~marcelk/pypovray/povray_basic.html)\]

    **Basic Povray Simulation Example**  
      
    This document describes the most basic usage of the **povray_simulation** Python package that is provided for this course. This library is used to render (*draw*) objects and create images, animations and simulations using the Povray ray-tracer (http://www.povray.org).

* ###[Pypovray Simulating - Part One](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/pypovray_simulation_1.ipynb) \[[mirror](https://bioinf.nl/~marcelk/pypovray/pypovray_simulation_1.html)\]

    **Creating Simulations with pypovray; a simple animation**
    
    Now that we have played a bit with positioning objects in 3D space, the next step will be animating objects in 3D space.

* ###[Povray Objects and Styling](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/povray_objects.ipynb) \[[mirror](https://bioinf.nl/~marcelk/pypovray/povray_objects.html)\]

    **Povray Objects, Styling and other modifiers**

    A summary showing an incomplete list of Povray objects that can be created using the `pypovray` project, how to apply different styles to these objects and some more advanced topics such as *scaling*, *moving* and *rotating* these objects. Most sections link to the official Povray documentation and other useful sources found online. 

The `pypovray` project functions as a translation layer between `Python`- and `Povray`-code as shown in the images below, where:
* the `povray` library from this repository is used to configure the project (render settings, file locations) as well as PDB-file rendering and
* the [Vapory library](http://zulko.github.io/blog/2014/11/13/things-you-can-do-with-python-and-pov-ray/) is used to translate the *Scene* constructed in `Python` code to actual `Povray` code.

![pypovray library](https://bitbucket.org/mkempenaar/pypovray/raw/master/manual/files/pypovray.png)

These code snippets show a single `Sphere` object placed in a `Scene` combined with a `Camera` and `LightSource`:

![py2povray](https://bitbucket.org/mkempenaar/pypovray/raw/master/manual/files/py2povray.png)

## Summary

To perform a clean install and use the template (**NOTE:** see [the installation manual](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/install_and_configure.ipynb) for a complete guide):

* Download the project using the *Downloads* link in the left-menu
* Extract the downloaded ZIP file
    * Open a terminal and go to the extracted folder
* Create a new Python virtual environment `virtualenv pypovray_venv`
    * Activate the venv: `source pypovray_venv/bin/activate`
* Install the required packages: `pip install -r requirements.txt`

The `template.py` and `simulation.py` scripts both produce movies taking six seconds (they an be looped). Running `python template.py` will create the output **GIF** movie file such as the one shown below.

![Template movie](https://bitbucket.org/mkempenaar/pypovray/raw/master/movies/template_md.gif)

The `template_pdb.py` file demonstrates the rendering of space-filled molecules originating from PDB files. The current version positions a molecule and rotates them on all axes resulting in the following output:

![Template movie](https://bitbucket.org/mkempenaar/pypovray/raw/master/movies/rotation_md.gif)

The `simulation.py` file has multiple arguments to render either an **MP4** or **GIF** movie file or a single frame by supplying a timepoint (in seconds): `python simulation.py --time 3.14 --mp4`. Use `-h` to see its help. Demonstrating the output of `simulation.py` (low-quality GIF file):

![Template movie](https://bitbucket.org/mkempenaar/pypovray/raw/master/movies/simulation_md.gif) 

The *images/* folder contains the output images after running the files; these will be emptied at the next run. Note that when creating an MP4 file the program will fail if a file with the same name already exists, this is the default *ffmpeg* behaviour.