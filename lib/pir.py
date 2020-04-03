from gpiozero import MotionSensor

class Motiondetector:
    def __init__(self):
        self.pir = MotionSensor(4)

    def detection(self):
        if self.pir.motion_detected:
            print("Motion")
            return True
        else:
            return False
