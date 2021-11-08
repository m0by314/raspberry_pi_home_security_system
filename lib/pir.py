""" Package for interfacing with Raspberry PI PIR motion sensor. """
import RPi.GPIO

PIR_PIN = 4

# Setup
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(PIR_PIN, RPi.GPIO.IN)


def movement_detected() -> bool:
    """Check if movement detected."""
    return RPi.GPIO.input(PIR_PIN)
