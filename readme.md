# A template project demonstrating the use of the Povray raytracer

To use the template:

* Download the project using the *Downloads* link in the left-menu
* Extract the downloaded ZIP file
    * Open a terminal and go to the extracted folder
* Create a new Python virtual environment `virtualenv pypovray`
    * Activate the venv: `source pypovray/bin/activate`
* Install the required packages: `pip install -r requirements.txt`

The `template.py` and `simulation.py` scripts both produce movies taking six seconds (they an be looped). Running `python template.py` will create the output **GIF** movie file such as the one shown below.

![Template movie](https://bitbucket.org/mkempenaar/povray_simulation/raw/master/template_md.gif) 

The `simulation.py` file has multiple arguments to render either an **MP4** or **GIF** movie file or a single frame by supplying a timepoint (in seconds): `python simulation.py --time 3.14 --mp4`. Use `-h` to see its help. Demonstrating the output of `simulation.py` (low-quality GIF file):

![Template movie](https://bitbucket.org/mkempenaar/povray_simulation/raw/master/simulation_md.gif) 

The *images/* folder contains the output images after running the files; these will be emptied at the next run. Note that when creating an MP4 file the program will fail if a file with the same name already exists, this is the default *ffmpeg* behaviour.