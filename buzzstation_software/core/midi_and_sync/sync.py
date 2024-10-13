import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
pin = 23
GPIO.setup(pin, GPIO.OUT)

def sync_out(pinBoolean):
    try:
        if pinBoolean:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
    except KeyboardInterrupt as exception:
        print(exception)
        GPIO.cleanup()

if __name__ == "__main__":
    # Tests
    while True:
        sync_out(True)
        time.sleep(0.1)
        sync_out(False)
        time.sleep(0.1)
