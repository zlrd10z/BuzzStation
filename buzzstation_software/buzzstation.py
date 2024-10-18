from threading import Thread
from libs.keypad import Keypad
from core.song_data import SongData
from core import playlist
from core.potentiometers_operations import pots_operations
import time
import os
import serial


# Remove all temporary audio files from .temp directory:
def clear_temp():
    cwd = os.getcwd()
    command = "rm " + cwd + "/.temp/* -f"
    os.system(command)

def main():
    # Clear temp dir:
    clear_temp()
    # Create objects:
    keys = Keypad()
    song_data = SongData()
    # open serial usb and put in song_data
    song_data.put_data('serial_usb', serial.Serial('/dev/ttyUSB0', 31250))
    #Create thread for potentiometers:
    thread_pots = Thread(target=pots_operations, args=[song_data])
    thread_pots.start()
    
    #main loop:
    playlist.main(keys, song_data)


if __name__ == "__main__":
    main()
