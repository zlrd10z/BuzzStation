import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

pin = 20
GPIO.setup(pin, GPIO.OUT)


def syncOut(pinBoolean):
	try:
		if pinBoolean:
			GPIO.output(pin, GPIO.HIGH)

		else:
			GPIO.output(pin, GPIO.LOW)


	except KeyboardInterrupt as exception:
		print(exception)
		GPIO.cleanup()




if __name__ == "__main__":
	while True:
		syncOut(True)
		time.sleep(0.1)
		syncOut(False)
		time.sleep(0.1)
