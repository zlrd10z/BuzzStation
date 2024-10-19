import RPi.GPIO as GPIO
import time
import sys


GPIO.setmode(GPIO.BCM)
pin = 23
GPIO.setup(pin, GPIO.OUT)

def sync_out():
    try:
        GPIO.output(pin, GPIO.HIGH)    
        GPIO.output(pin, GPIO.LOW)
    except KeyboardInterrupt as exception:
        print(exception)
        GPIO.cleanup()
