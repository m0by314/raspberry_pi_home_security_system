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
    def __init__(self, camera, folder: str):
        self.__camera = camera
        self.__registration_folder = os.path.abspath(folder)

    def start_recording(self, delay=60):
        """
        Starts recording the video for a time defined by a delay parameter.

        :param delay: recording time
        :return: video at mp4 format
        """
        video_h264 = os.path.join(self.__registration_folder,
                                  'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.h264')
        video_mp4 = os.path.join(self.__registration_folder,
                                 'vid-' + time.strftime("%H%M%S-%Y%m%d") + '.mp4')
        self.__camera.start_recording(video_h264)
        time.sleep(int(delay))
        self.__camera.stop_recording()

        # convert video at mp4 format
        self.__convert_h264_to_mp4(video_h264, video_mp4)
        return video_mp4

    def __convert_h264_to_mp4(self, h264, mp4):
        """
        Converted video format h264 in mp4.

        :raise: OSError
        """
        command = F"MP4Box -add {h264} {mp4}"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            print(F'FAIL:\ncmd:{err.cmd}\noutput:{err.output}')
            raise OSError from subprocess.CalledProcessError

        # remove h264 file after convert to mp4 format
        self._remove_file(h264)

    @staticmethod
    def _remove_file(file):
        """
        Remove a specific file

        :raise OSError
        """
        remove_cmd = F"rm {file}"
        try:
            subprocess.check_output(remove_cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            print(F'FAIL:\ncmd:{err.cmd}\noutput:{err.output}')
            raise OSError from subprocess.CalledProcessError

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

        :return: string result
        :raise: OSError
        """
        command = "cd " + self.__registration_folder + " && rm -f *"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as err:
            print(F'FAIL:\ncmd:{err.cmd}\noutput:{err.output}')
            raise OSError from subprocess.CalledProcessError
        else:
            return str('The records have been deleted')

    def __del__(self):
        self.__camera.close()
