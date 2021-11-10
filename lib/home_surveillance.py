"""Home Surveillance packages"""
import signal


class HomeSurveillance:
    """
    Class to interact with the Home Surveillance

    :param camera: Camera instance.
    :param bot: PrivateBot instance.
    :param motion_detector: boolean function return True if a movement is detected
    """
    def __init__(self, camera, bot, motion_detector):
        self._camera = camera
        self._bot = bot
        self._motion_detector = motion_detector

        # Status of the HomeSurveillance
        self._is_start = False

        # Status for signal closing
        self.__is_close = False

        # Action for signal SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self._close)
        signal.signal(signal.SIGTERM, self._close)

    @property
    def is_close(self):
        """Signal closing status"""
        return self.__is_close

    def _close(self, *args):
        """Handler for signal.signal"""
        self.__is_close = True

    @property
    def is_start(self) -> bool:
        """Home Surveillance Status."""
        return bool(self._is_start)

    def start(self):
        """Home Surveillance Start."""
        self._is_start = True

    def stop(self):
        """Home Surveillance Stop."""
        self._is_start = False

    def run(self):
        """
        Motion detection, if motion is detected and surveillance is activated
        a video recording is taken and sent through the telegram bot
        """
        if self.is_start and self._motion_detector():
            try:
                with open(self._camera.start_recording(), 'rb') as video_file:
                    self._bot.send_video(video_file)
            except SystemError as err:
                self._bot.send_message(err)
