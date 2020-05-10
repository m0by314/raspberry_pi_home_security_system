"""
Package for interfacing with Raspberry PI camera.
"""
import subprocess
import time
import os

from picamera import PiCamera


class Camera:
    """
    Class to interfaces with Raspberry Pi Camera module.
    Photos and videos are named photo-%H%M%S-%Y%m%d.jpeg and vid-%H%M%S-%Y%m%d.mp4 respectively.

    :param folder: allows you to define the folder where the records are stored.
    """

    def __init__(self, folder):
        self.camera = PiCamera()
        self.registration_folder = folder
        self.record = {}

    def start_recording(self, delay=60):
        """
        Starts recording the video for a time defined by a delay parameter.

        :param delay: recording time
        :return: dictionary containing the name of the video and the return code of the recording.
        """
        video_h264 = os.path.join(self.registration_folder,
                                  'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.h264')
        video_mp4 = os.path.join(self.registration_folder,
                                 'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.mp4')
        self.camera.start_recording(video_h264)
        time.sleep(int(delay))
        self.camera.stop_recording()

        error = self.__convert_h264_to_mp4(video_h264, video_mp4)
        self.record = {
            "name": video_mp4,
            "return_code": error,
        }
        return self.record

    @staticmethod
    def __convert_h264_to_mp4(h264, mp4):
        """
        Converted the video format h264 in mp4.

        :return: error message if conversion is in fail or None
        """
        command = "MP4Box -add {} {}".format(h264, mp4)
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            error = 'FAIL:\ncmd:{}\noutput:{}'.format(err.cmd, err.output)
            return error
        else:
            return None

    def take_photo(self):
        """
        Take a photo.

        :return: photo at format .jpeg
        """
        photo = os.path.join(self.registration_folder, 'photo-' +
                             time.strftime("%H%M%S-%Y%m%d") + '.jpeg')
        self.camera.capture(photo)
        return photo

    def __del__(self):
        self.camera.close()

    def purge_records(self):
        """
        Deletes records from the folder.

        :return: deletion result
        """
        command = "cd " + self.registration_folder + " && rm *"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            result = 'FAIL:\ncmd:{}\noutput:{}'.format(err.cmd, err.output)
            return result
        else:
            result = 'The records have been deleted'
            return result
