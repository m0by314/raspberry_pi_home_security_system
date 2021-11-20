"""Home Surveillance class"""
import signal


class HomeSurveillance:
    """
    Class to keep the specific status required by the application. Avoid the use of \"global\".

    Specific status:
        _is_start:     if true the intrusion detection is activated
        _interrupted:  status to stop the infinite loop of motion detection.
    """
    def __init__(self):
        # Status
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
        """Return interrupted status"""
        return self._interrupted

    @property
    def is_start(self) -> bool:
        """Return is_start status."""
        return bool(self._is_start)

    def start(self):
        """Start intrusion detection."""
        self._is_start = True

    def stop(self):
        """Stop intrusion detection."""
        self._is_start = False
