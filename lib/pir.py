""" Package for interfacing with Raspberry PI PIR motion sensor. """
from gpiozero import MotionSensor

pir = MotionSensor(4)


def motion_detected() -> bool:
    """Check if motion detected."""
    return bool(pir.motion_detected)