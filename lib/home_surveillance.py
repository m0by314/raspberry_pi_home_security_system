"""Home Surveillance packages"""


class HomeSurveillance:
    """Class to interact with the Home Surveillance"""

    def __init__(self):
        self._is_start = False

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
