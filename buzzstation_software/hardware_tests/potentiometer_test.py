import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# I2C bus initialization:
i2c = busio.I2C(board.SCL, board.SDA)

# ADS1115 initialization:
ads = ADS.ADS1115(i2c, address = 0x48)

# Channels initialization:
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

# Reading values from the channels:
while True:
    print("----------------")
    print("A0: " + str(chan0.voltage))
    print("A1: " + str(chan1.voltage))
    print("A2: " + str(chan2.voltage))
    print("----------------")
    time.sleep(0.5)
