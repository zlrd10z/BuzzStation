import RPi.GPIO as GPIO
import time


class Keypad():
    GPIO.setmode(GPIO.BCM)
    cols = [6, 0, 19]
    rows = [5, 21, 26, 13]

    # Pins setup:
    for i in range(len(cols)):
        GPIO.setup(cols[i], GPIO.OUT)
    for i in range(len(rows)):
        GPIO.setup(rows[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


    keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
    ]

    def check_keys(self):
        try:
            key = ""
            for i in range(len(self.cols)):
                GPIO.output(self.cols[i], GPIO.LOW)
                time.sleep(0.01)
                for j in range(len(self.rows)):
                    if not GPIO.input(self.rows[j]):
                        time.sleep(0.01)
                        if not GPIO.input(self.rows[j]):
                            key = self.keys[j][i]
                        while not GPIO.input(self.rows[j]):
                            pass
                GPIO.output(self.cols[i], GPIO.HIGH)
                time.sleep(0.01)
            return key
        except Exception as e:
            print(e)
            GPIO.cleanup()

if __name__ == "__main__":
	#tests:
	while True:
			keypad = Keypad()
			key = keypad.check_keys()
			if key != "":
					print(key)
