import time
from keypad import Keypad
import spi


k = Keypad()
while True:
    key = k.check_keys()
    if key != "":
        print(key)

        spi.sendByte(int(key.encode("utf-8").hex(), 16))
        time.sleep(0.01)
    time.sleep(0.01)

