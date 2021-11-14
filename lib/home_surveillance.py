"""Home Surveillance class"""
import signal


class HomeSurveillance:
    """Class to interact with the Home Surveillance"""
    def __init__(self):
        # Status of the HomeSurveillance
        self._is_start = False
        self._interrupted = False

        # Action for signal SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, *args):
        """Handler for signal.signal"""
        print("\nExiting HomeSurveillance")
        self._interrupted = True

    @property
    def is_interrupted(self) -> bool:
        """Home Surveillance interrupted"""
        return self._interrupted

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
