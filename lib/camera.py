import subprocess
import time
import os

from picamera import PiCamera


class Camera:
    """
    Class to interfaces with Raspberry Pi Camera module

    :param registration_folder: folder path for video recording
    :param video_time: recording time
    """

    def __init__(self, video_time=20):
        self.camera = PiCamera()
        self.registration_folder = 'tmp/video'
        self.photo = os.path.join(self.registration_folder, 'photo' + time.strftime("%H%M%S-%Y%m%d") + '.jpeg')
        self.video_time = video_time
        self.record = {}

    def start_recording(self):
        """
        Starts the recording of the video
        :return: dictionary containing the name of the video and the return code of the recording.
        """
        self.video = os.path.join(self.registration_folder, 'vid-' + time.strftime("%H%M%S-%Y%m%d"))
        self.video_h264 = self.video + '.h264'

        self.camera.start_recording(self.video_h264)
        time.sleep(self.video_time)
        self.camera.stop_recording()

        error = self.__convert_h264_to_mp4()
        self.record = {
            "name": self.video_mp4,

            "return_code": error,
        }
        return self.record

    def __convert_h264_to_mp4(self):
        """
        Converted the video format h264 in mp4
        return error message if conversion is in fail
        """
        self.video_mp4 = self.video + '.mp4'

        command = "MP4Box -add {} {}".format(self.video_h264, self.video_mp4)
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            error = 'FAIL:\ncmd:{}\noutput:{}'.format(err.cmd, err.output)
            return error
        else:
            return 0

    def take_photo(self):
        self.camera.capture(self.photo)
        return self.photo

    def __del__(self):
        self.camera.close()

    def purge_records(self):
        """
        Deletes records from the folder
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
