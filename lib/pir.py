#! /usr/bin/python3

from gpiozero import MotionSensor


class Motion:
    def __init__(self):
        self.pir = MotionSensor(4)

    def detection(self):
        if self.pir.motion_detected:
            print("Motion")
            return True
        else:
            return False
