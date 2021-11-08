""" Package for interfacing with Raspberry PI PIR motion sensor. """
import RPi.GPIO as GPIO

PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIR_PIN, GPIO.IN)


def movement_detected() -> bool:
    """Check if movement detected."""
    return GPIO.input(PIR_PIN)
