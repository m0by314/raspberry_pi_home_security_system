""" Package for interfacing with Raspberry PI PIR motion sensor. """
from gpiozero import MotionSensor

pir = MotionSensor(4)


def movement_detected() -> bool:
    """Check if movement detected."""
    return bool(pir.motion_detected)
