#! /usr/bin/python3

import subprocess
import time
import os

from picamera import PiCamera


class Camera:
    """
    Class for using picamera
    """

    def __init__(self, video_path, video_time=20):
        self.camera = PiCamera()
        self.path = video_path
        self.selfie_name = os.path.join(video_path, 'selfie.jpeg')
        self.video_time = video_time

    def start_record(self):
        """
        start record during 20s,
        return video name at mp4 format or error if convert fail
        """
        self.file = os.path.join(self.path, 'intrusion-' + time.strftime("%H%M%S-%Y%m%d"))
        self.file_h264 = self.file + '.h264'
        self.file_mp4 = self.file + '.mp4'

        self.camera.start_recording(self.file_h264)
        time.sleep(self.video_time)
        self.camera.stop_recording()

        error = self.__convert_h264_to_mp4()
        if error == 0:
            return {0: self.file_mp4}
        else:
            return {1: error}

    def __convert_h264_to_mp4(self):
        """
        convert format h264 in mp4
        return error message if convertion is in fail
        """
        command = "MP4Box -add {} {}".format(self.file_h264, self.file_mp4)
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as error:
            err = 'FAIL:\ncmd:{}\noutput:{}'.format(error.cmd, error.output)
            return err
        else:
            return 0

    def selfie(self):
        self.camera.capture(self.selfie_name)
        return self.selfie_name

    def __del__(self):
        self.camera.close()
