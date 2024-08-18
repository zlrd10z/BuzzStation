import time
import board
import busio
from adafruit_ads1x15 import ads1115
from adafruit_ads1x15.analog_in import AnalogIn

# I2C init:
i2c = busio.I2C(board.SCL, board.SDA)

# ADS1115 init:
ads = ADS.ADS1115(i2c, address = 0x4a)

# Channels init:
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

def returnPotentiometersValues():
	return chan0.voltage, chan1.voltage, chan2.voltage

