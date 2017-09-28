"""
This module offers functionality to render a frame or movie given a
Vapory 'Scene' object.
"""

import ffmpy
import shutil
import sys
import os
from pathos.multiprocessing import ProcessingPool as Pool
from moviepy.editor import ImageSequenceClip
from tempfile import mkdtemp
from glob import glob
from povray import SETTINGS, logger
from distutils import util


def render_scene_to_png(scene, frame_id=0):
    """ Renders a single frame given the `scene` function object and either a time in seconds
     or a frame number which is passed to the `scene` function """
    folder = _create_tmp_folder()
    _render_frame(scene(frame_id), frame_id)

    if SETTINGS.LogLevel != "DEBUG":
        shutil.rmtree(folder)


def render_scene_to_gif(scene):
    """ Creates a GIF output 'movie' using moviepy.
    NOTE: a GIF file has reduced quality compared to the rendered output!
    """

    if _check_output_file_exists("gif"):
        logger.error('["%s"] - Not simulating; output file already exists.',
                     sys._getframe().f_code.co_name)
        return
    # Render the scenes (creates PNG images in the SETTINGS.OutputImageDir folder)
    _render_scene(scene)

    # Get a list of all rendered images (these are ordered by default)
    image_files = glob('{}/{}_*.png'.format(SETTINGS.OutputImageDir, SETTINGS.OutputPrefix))
    # Combine images into GIF file using moviepy
    ImageSequenceClip(sorted(image_files),
                      fps=SETTINGS.RenderFPS).write_gif('{}/{}.gif'.format(SETTINGS.OutputMovieDir,
                                                                           SETTINGS.OutputPrefix))


def render_scene_to_mp4(scene):
    """ Creates a high-quality MP4 movie using 'ffmpeg' """

    if _check_output_file_exists("mp4"):
        logger.error('["%s"] - Not simulating; output mp4 file already exists.',
                     sys._getframe().f_code.co_name)
        return

    if _check_rendered_images():
        logger.error('["%s"] - Not simulating; output image file(s) already exist.',
                     sys._getframe().f_code.co_name)
        return

    # Render the scenes (creates PNG images in the SETTINGS.OutputImageDir folder)
    _render_scene(scene)

    # Combine the frames into a movie
    _run_ffmpeg()


def _render_scene(scene):
    """ Renders the scene to multiple output PNG files for use in animations """

    # Clear 'images' folder containing previously rendered frames
    #_remove_folder_contents(SETTINGS.OutputImageDir)

    # Calculate the time per frame (i.e. evaluate expression from config file)
    nframes = eval(SETTINGS.NumberFrames)

    # Render each scene using a thread pool or single-threaded
    if util.strtobool(SETTINGS.UsePool):
        scene_flist = [scene] * nframes
        id_list = range(nframes)

        # Render each scene, using a thread pool
        with Pool(int(SETTINGS.workers)) as p:
            p.map(render_scene_to_png, scene_flist, id_list)

    else:
        for frame_id in range(nframes):
            render_scene_to_png(scene, frame_id)


def _remove_folder_contents(folder, match=None):
    """ Cleans up folder contents """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                if match:
                    if match in the_file:
                        os.unlink(file_path)
                else:
                    os.unlink(file_path)
        except Exception as e:
            print(e)


def _render_frame(scene, frame_id):
    """ Renders a single frame """
    frame_file = _create_frame_file_name(frame_id)
    scene.render(frame_file,
                 width=SETTINGS.ImageWidth,
                 height=SETTINGS.ImageHeight,
                 antialiasing=SETTINGS.AntiAlias,
                 quality=SETTINGS.Quality, remove_temp=False)


def _create_tmp_folder():
    tmp_folder = mkdtemp()
    os.chdir(tmp_folder)
    logger.debug('["%s"] - tmp_folder: %s', sys._getframe().f_code.co_name, tmp_folder)
    return tmp_folder


def _create_frame_file_name(frame):
    output_file = '{}/{}_{}.png'.format(SETTINGS.OutputImageDir,
                                        SETTINGS.OutputPrefix, str(round(frame, 2)).zfill(3))
    logger.debug('["%s"] - output file: %s', sys._getframe().f_code.co_name, output_file)
    return output_file


def _check_output_file_exists(extension):
    """ Informs about existing output file before creating a new one
    and offers to overwrite the existing file. """
    output_file = '{}/{}.{}'.format(SETTINGS.OutputMovieDir,
                                    SETTINGS.OutputPrefix, extension)
    remove_file = "n"
    if os.path.exists(output_file):
        remove_file = str(input("The file '%s' already exists, do you want to overwrite? (y/n): " % output_file))
    if remove_file.lower() == "y":
        os.remove(output_file)

    return os.path.exists(output_file)


def _check_rendered_images():
    """ Informs about existing output image files before rendering
    and offers to overwrite the existing file. """
    remove_files = "n"
    if os.listdir(SETTINGS.OutputImageDir):
        if any(SETTINGS.OutputPrefix in fname for fname in os.listdir(SETTINGS.OutputImageDir)):
            remove_files = str(input("Image files already exists in %s, " % SETTINGS.OutputImageDir +
                                     "do you want to overwrite? (y/n): "))
    if remove_files.lower() == "y":
        _remove_folder_contents(SETTINGS.OutputImageDir, match=SETTINGS.OutputPrefix)

    return any(SETTINGS.OutputPrefix in fname for fname in os.listdir(SETTINGS.OutputImageDir))


def _run_ffmpeg():
    """ Builds the ffmpeg command to render an MP4 movie file using the
    h.x264 codex and yuv420p format """
    ff = ffmpy.FFmpeg(
        # Input is a pattern for all image files ordered by number (padded)
        inputs={'': '-framerate {} -pattern_type glob -i {}/{}_*.png'.format(
            SETTINGS.MovieFPS,
            SETTINGS.OutputImageDir,
            SETTINGS.OutputPrefix)},
        outputs={'{}/{}.mp4'.format(SETTINGS.OutputMovieDir,
                                    SETTINGS.OutputPrefix):
                     '-c:v libx264 -r 30 -crf 2 -pix_fmt yuv420p ' +
                     '-loglevel warning'}
    )
    # Run ffmpeg and create output movie file
    logger.info('["%s"] - ffmpeg command: "%s"', sys._getframe().f_code.co_name, ff.cmd)
    ff.run()
