"""Home Surveillance packages"""
import signal
import time


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

        # Infinite loop is running status
        self.__loop_run = True

        # Action for signal SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    @property
    def loop_is_run(self):
        """Show status of infinity loop run"""
        return self.__loop_run

    def _signal_handler(self, *args):
        """Handler for signal.signal"""
        print("\nExiting HomeSurveillance")
        self.__loop_run = False

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

    def run_loop(self):
        """
        Run infinite loop for Motion detection, if motion is detected and surveillance is activated
        a video recording is taken and sent through the telegram bot
        """
        while self.__loop_run:
            if self.is_start and self._motion_detector:
                try:
                    with open(self._camera.start_recording(), 'rb') as video_file:
                        self._bot.send_video(video_file)
                except SystemError as err:
                    self._bot.send_message(err)
            time.sleep(1)
