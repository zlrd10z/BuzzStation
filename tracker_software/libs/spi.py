import spidev
import time
import RPi.GPIO as GPIO

def spiInit():
      # Inicjalizacja interfejsu SPI
      spi = spidev.SpiDev(0, 0)
      spi.open(0, 0)  # Otwarcie urządzenia SPI /dev/spidev0.0
      spi.max_speed_hz = 5000
      spi.mode = 0
      spi.bits_per_word = 8
      spi.lsbfirst = False
      return spi

spi = spiInit()

def sendByte(byte):
    bytes_to_send = bytes([byte])
    spi.writebytes(bytes_to_send)

