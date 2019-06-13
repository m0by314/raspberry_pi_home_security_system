#! /usr/bin/python3

from gpiozero import MotionSensor

class Motion():
    def __init__(self, cam):
        self.pir = MotionSensor(4)
        self.camera = cam

    def detection(self):
        if self.pir.motion_detected:
            print("Motion")
            self.camera.start_record()
