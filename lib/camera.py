""" Package for interfacing with Raspberry PI camera. """
import subprocess
import time
import os


class Camera:
    """
    Class to interfaces with Raspberry Pi Camera module.
    Photos and videos are named photo-%H%M%S-%Y%m%d.jpeg and vid-%H%M%S-%Y%m%d.mp4 respectively.

    :param folder: allows you to define the folder where the records are stored.
    """
    def __init__(self, camera, folder: str, delay: int):
        self.__camera = camera
        self.__registration_folder = os.path.abspath(folder)
        self.__delay = delay

    def start_recording(self, delay=None):
        """
        Starts recording the video for a time defined by a delay parameter.

        :param delay: recording time
        :return: video at mp4 format
        """
        if delay is None:
            delay = self.__delay

        video_h264 = os.path.join(self.__registration_folder,
                                  'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.h264')
        video_mp4 = os.path.join(self.__registration_folder,
                                 'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.mp4')
        self.__camera.start_recording(video_h264)
        time.sleep(int(delay))
        self.__camera.stop_recording()

        return self.__convert_h264_to_mp4(video_h264, video_mp4)

    @staticmethod
    def __convert_h264_to_mp4(h264, mp4):
        """
        Converted the video format h264 in mp4.

        :raise: SystemError
        """
        command = F"MP4Box -add {h264} {mp4}"
        try:
            video_converted = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            print(F'FAIL:\ncmd:{err.cmd}\noutput:{err.output}')
            raise SystemError from subprocess.CalledProcessError
        return video_converted

    def take_photo(self):
        """
        Take a photo.

        :return: photo at format .jpeg
        """
        photo = os.path.join(self.__registration_folder, 'photo-' +
                             time.strftime("%H%M%S-%Y%m%d") + '.jpeg')
        self.__camera.capture(photo)
        return photo

    def purge_records(self):
        """
        Deletes records from the folder.

        :return: deletion result
        :raise: SystemError
        """
        command = "cd " + self.__registration_folder + " && rm -f *"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            print(F'FAIL:\ncmd:{err.cmd}\noutput:{err.output}')
            raise SystemError from subprocess.CalledProcessError
        else:
            return str('The records have been deleted')

    def __del__(self):
        self.__camera.close()
