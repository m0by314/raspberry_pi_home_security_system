#! /usr/bin/python3
# Lib for camera action

import subprocess
import time

from picamera  import PiCamera
from .local    import video_path, selfie_path

camera = PiCamera()

def start_record():
    """
    start record during 20s,
    return video name at mp4 format or error if convert fail
    """

    timestr = time.strftime("%H%M%S-%Y%m%d")
    file = video_path + timestr
    file_h264 = file + '.h264'
    file_mp4  = file + '.mp4'

    camera.start_recording(file_h264)
    time.sleep(20)
    camera.stop_recording()

    error = _convert_h264_to_mp4(file_h264, file)
    if error == 0:
        return { 0 : file_mp4 }
    else:
        return { 1 : error }


def _convert_h264_to_mp4(file_h264, file):
    """
    convert format h264 in mp4
    return error message if convertion is in fail
    """

    command = "MP4Box -add {} {}.mp4".format(file_h264, file)
    try:
      output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
      err = 'FAIL:\ncmd:{}\noutput:{}'.format(error.cmd, error.output)
      return err
    else:
      return 0

def selfie():
    camera.capture(selfie_path)
    return selfie_path
