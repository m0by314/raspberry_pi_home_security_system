#! /usr/bin/python3

from gpiozero import MotionSensor
from camera import Camera

pir = MotionSensor(4)

class Motion(Camera):
    def __init__(self):
        super().__init__()
        self.pir = MotionSensor(4)

    def detection(self):
        if self.pir.motion_detected:
            print("Motion")
            self.start_record()
         
       
            
    
