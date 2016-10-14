from tempfile import mkdtemp
from glob import glob
from povray import SETTINGS
from povray.models import *
import configparser
import os


def make_frame(t, scene, time, i=None):
    ''' Runs Povray through the vapory library for the frame at time t '''
    ## TODO: create temporary location for image storage if creating a movie

    # If no frame number is given, use time t
    if not i:
        i = t

    # Define file name to store current frame in
    frame_file = '{}/{}_{}.png'.format(SETTINGS.OutputImageDir,
                                          SETTINGS.OutputPrefix, str(i).zfill(3))
    
    # If t does not represent a timepoint, use i instead
    if time:
        t = i

    # Run Povray
    scene(t).render(frame_file,
                    width=SETTINGS.ImageWidth,
                    height=SETTINGS.ImageHeight,
                    antialiasing=SETTINGS.AntiAlias,
                    quality=SETTINGS.Quality, remove_temp=False)

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
    timepoints = [i * ftime for i in range(int(SETTINGS.Duration) * int(SETTINGS.RenderFPS))]
    
    # Render each scene
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
    ImageSequenceClip(image_files, fps=SETTINGS.RenderFPS).write_gif('{}.gif'.format(SETTINGS.OutputPrefix))

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
