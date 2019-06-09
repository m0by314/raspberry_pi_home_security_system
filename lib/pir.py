#! /usr/bin/python3

from gpiozero import MotionSensor
import camera

pir = MotionSensor(4)

class Motion():
    def __init__(self):
        self.pir = MotionSensor(4)
        self.camera = None
        self.bot = None
        
    def __camera(self):
        """
        create camera instance
        """
        if self.camera is None:
            self.camera = camera.Camera() #TODO Add args

        return self.camera
        
    def detection(self):
        if self.pir.motion_detected:
            print("Motion")
            self.camera.start_record()
         
       
            
    
