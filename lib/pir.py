from gpiozero import MotionSensor


class Motiondetector:
    """
    Class to interfaces with Raspberry PIR motion sensor module
    """

    def __init__(self):
        self.pir = MotionSensor(4)

    def movement_detected(self):
        if self.pir.motion_detected:
            return True
        else:
            return False
