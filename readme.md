# A template project demonstrating the use of the Povray raytracer

## Manuals

* ###[Installing and Configuring](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/install_and_configure.ipynb)

    **Guide for Installing and Configuring the software**  
      
    This short document describes how to get the required software (mainly, this Python package), configure it and run one of the included examples on the Bioinformatics computer network. At the bottom of the document is a section on how to do this on your own computer.

* ###[Basic usage of PyPovray](http://nbviewer.jupyter.org/urls/bitbucket.org/mkempenaar/pypovray/raw/master/manual/povray_basic.ipynb)

    **Basic Povray Simulation Example**  
      
    This document describes the most basic usage of the **povray_simulation** Python package that is provided for this course. This library is used to render (*draw*) objects and create images, animations and simulations using the Povray ray-tracer (http://www.povray.org).

## Usage

To use the template:

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