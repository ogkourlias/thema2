from povray.settings import *
from tempfile import mkdtemp
from glob import glob
import os

def make_frame(t, scene, time, i=None):
    ''' Runs Povray through the vapory library for the frame at time t '''
    ## TODO: create temporary location for image storage if creating a movie
    # If no frame number is given, use time t
    if not i:
        i = t
    # Define file name to store current frame in
    frame_file = '{}/{}/{}_{}.png'.format(file_dir, imagefile_dir,
                                          outfile_prefix, str(i).zfill(3))
    
    # If t does not represent a timepoint, use i instead
    if time:
        t = i
    # Run Povray
    scene(t).render(frame_file, width=iwidth, height=iheight,
                    antialiasing=antialias, quality=quality, remove_temp=True)

def remove_folder_contents(folder):
    '''Cleans up folder contents'''
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def render_scene(scene, time):
    ''' Renders the scenes to output PNG files '''
    # Clear 'images' folder containing the frames
    remove_folder_contents("images/")

    # Pre-build scene times, one per frame
    t = [i * ftime for i in range(duration * sfps)]
    for i, frame in enumerate(t):
        make_frame(frame, scene, time, i+1)

def render_scene_to_gif(scene, render_mp4=False, time=True):
    ''' Creates a GIF output 'movie' given the PNG renders
    NOTE: a GIF file has reduced quality compared to the rendered output!
    '''
    render_scene(scene, time)

    # Import moviepy to stitch the files into a GIF
    from moviepy.editor import ImageSequenceClip

    # Combine images into GIF file using moviepy
    f = glob('{}/{}_*.png'.format(imagefile_dir, outfile_prefix))
    ImageSequenceClip(f, fps=sfps).write_gif('{}.gif'.format(outfile_prefix))

def render_scene_to_mp4(scene, render_gif=False, time=True):
    ''' Creates a high-quality MP4 movie using 'ffmpeg' '''
    # Render the scenes, if no GIF file has been created
    if not render_gif:
        render_scene(scene, time)

    # Import Python ffmpeg wrapper
    import ffmpy
    ff = ffmpy.FFmpeg(
            # Input is a pattern for all image files ordered by number (padded)
            inputs={'{}/{}_%03d.png'.format(imagefile_dir, outfile_prefix):'-framerate 25'},
            outputs={'movies/{}.mp4'.format(outfile_prefix):'-c:v libx264 -r 30 -crf 2 -pix_fmt yuv420p'}
         )
    # Run ffmpeg and create output movie file
    ff.run()