import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Inicjalizacja magistrali I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicjalizacja ADS1115
ads = ADS.ADS1115(i2c, address = 0x4a)

# Inicjalizacja kanału (np. AIN0)
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

# Odczyt wartości z kanału
while True:
	print("----------------")
	print("A0: " + str(chan0.voltage))
	print("A1: " + str(chan1.voltage))
	print("A2: " + str(chan2.voltage))
	print("----------------")
	time.sleep(0.5)
