import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# I2C init:
i2c = busio.I2C(board.SCL, board.SDA)

# ADS1115 init:
ads0 = ADS.ADS1115(i2c, address = 0x48)
ads1 = ADS.ADS1115(i2c, address = 0x4b)

# Channels init:
chan1_0 = AnalogIn(ads1, ADS.P0)
chan0_2 = AnalogIn(ads0, ADS.P1)
chan0_3 = AnalogIn(ads0, ADS.P2)

def return_potentiometers_values():
    return chan1_0.voltage, chan0_2.voltage, chan0_3.voltage

def return_p1_val():
    return chan1_0.voltage