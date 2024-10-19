from threading import Thread
import multiprocessing
from libs.keypad import Keypad
from core.song_data import SongData
from core import playlist
from core.potentiometers_operations import pots_operations
from core.player_proc import player_audiofiles
import time
import os
from core import player
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

    # Create serial_usb:
    serial_usb = serial.Serial('/dev/ttyUSB0', 31250)
    song_data.put_data('serial_usb', serial_usb)

    # Create audio files player in another process:
    queue_player = multiprocessing.Queue()
    song_data.put_data('queue_player', queue_player)
    proc_player = multiprocessing.Process(target=player_audiofiles, args=(queue_player,))

    # Create thread for potentiometers:
    thread_pots = Thread(target=pots_operations, args=[song_data])
    thread_pots.start()

    # Create thread for note player:
    thread_player = Thread(target=player.main_loop, args=[song_data])
    thread_player.start()

    # Playlist Loop:
    playlist.main(keys, song_data)

if __name__ == "__main__":
    main()
