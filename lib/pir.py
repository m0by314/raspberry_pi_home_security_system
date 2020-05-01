"""
Pir library
"""
from gpiozero import MotionSensor


class Motiondetector:  # pylint: disable=too-few-public-methods
    """
    Class to interfaces with Raspberry PIR motion sensor module
    """

    def __init__(self):
        self.pir = MotionSensor(4)

    def movement_detected(self):
        """
        check if movement detected
        :return:
        """
        return bool(self.pir.motion_detected)
