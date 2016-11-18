from tempfile import mkdtemp
from glob import glob
from povray import SETTINGS
from povray.models import *
import configparser
import distutils
import shutil
import os

# Python multiprocessing using extended pickle serialization with
# dill: https://github.com/uqfoundation/dill
# and pathos: https://github.com/uqfoundation/pathos

from pathos.multiprocessing import ProcessingPool as Pool

def make_frame(t, scene, time, i=None):
    ''' Runs Povray through the vapory library for the frame at time t '''
    # If no frame number is given, use time t
    if not i:
        i = t

    # Define file name to store current frame in
    frame_file = '{}/{}_{}.png'.format(SETTINGS.OutputImageDir,
                                          SETTINGS.OutputPrefix, str(i).zfill(3))

    # If t does not represent a timepoint, use i instead
    if not time:
        t = i

    # Change working directory to temp location, one for each 'worker' in the Pool         
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)

    # Run Povray
    scene(t).render(frame_file,
                    width=SETTINGS.ImageWidth,
                    height=SETTINGS.ImageHeight,
                    antialiasing=SETTINGS.AntiAlias,
                    quality=SETTINGS.Quality, remove_temp=False)

    # Remove temp folder
    shutil.rmtree(tmp_folder)

def _remove_folder_contents(folder):
    '''Cleans up folder contents'''
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def _render_scene(scene, time):
    ''' Renders the scenes to output PNG files '''
    # Clear 'images' folder containing previously rendered frames
    _remove_folder_contents("images/")

    # Calculate the time per frame (i.e. evaluate expression from config file)
    ftime = eval(SETTINGS.FrameTime)
    # Pre-build scene times, one per frame
    timepoints = [i * ftime for i in range(int(SETTINGS.Duration * SETTINGS.RenderFPS))]

    if distutils.util.strtobool(SETTINGS.UsePool):
      # TODO: map the objects in a more efficient way to the make_frame method
      scene_flist = [scene for i in range(len(timepoints))]
      time_list = [time for i in range(len(timepoints))]
      i_list = [i+1 for i in range(len(timepoints))]

      # Render each scene, using a thread pool
      with Pool(int(SETTINGS.workers)) as p:
        # All arguments except the first must have the same length
        p.map(make_frame, timepoints, scene_flist, time_list, i_list)

    else:
      # Render each scene using single thread
      for i, frame in enumerate(timepoints):
          make_frame(frame, scene, time, i+1)

def render_scene_to_gif(scene, render_mp4=False, time=True):
    ''' Creates a GIF output 'movie' given the PNG renders
    NOTE: a GIF file has reduced quality compared to the rendered output!
    '''
    # Render the scenes (creates PNG images in the SETTINGS.OutputImageDir folder)
    _render_scene(scene, time)

    # Import moviepy to stitch the files into a GIF
    from moviepy.editor import ImageSequenceClip

    # Get a list of all rendered images (these are ordered by default)
    image_files = glob('{}/{}_*.png'.format(SETTINGS.OutputImageDir, SETTINGS.OutputPrefix))
    # Combine images into GIF file using moviepy
    ImageSequenceClip(sorted(image_files),
                      fps=SETTINGS.RenderFPS).write_gif('{}.gif'.format(SETTINGS.OutputPrefix))

def render_scene_to_mp4(scene, render_gif=False, time=True):
    ''' Creates a high-quality MP4 movie using 'ffmpeg' '''
    # Render the scenes only if no GIF file has already been created
    if not render_gif:
        _render_scene(scene, time)

    # Import Python ffmpeg wrapper
    import ffmpy
    
    # Build the ffmpeg command to render an MP4 movie file using the h.x264 codex and yuv420p format
    ff = ffmpy.FFmpeg(
            # Input is a pattern for all image files ordered by number (padded)
            inputs={'{}/{}_%03d.png'.format(SETTINGS.OutputImageDir, 
                                            SETTINGS.OutputPrefix):'-framerate {}'.format(SETTINGS.MovieFPS)},
            outputs={'{}/{}.mp4'.format(SETTINGS.OutputMovieDir, 
                                        SETTINGS.OutputPrefix):'-c:v libx264 -r 30 -crf 2 -pix_fmt yuv420p'}
         )
    # Run ffmpeg and create output movie file
    ff.run()
