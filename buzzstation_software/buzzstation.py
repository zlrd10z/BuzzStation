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
import logging


# Remove all temporary audio files from .temp directory:
def clear_temp():
    cwd = os.getcwd()
    command = "rm " + cwd + "/.temp/* -f"
    os.system(command)

def default_dirs():
    cwd = os.getcwd()
    if not os.path.isdir(cwd + '/samples'):
        os.system('mkdir ' + cwd + '/samples')
    if not os.path.isdir(cwd + '/saved_songs'):
        os.system('mkdir ' + cwd + '/saved_songs')
    if not os.path.isdir(cwd + '/.temp'):
        os.system('mkdir ' + cwd + '/.temp')

def main():

    logging.basicConfig(filename='errors.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s'
                        )
    # Clear temp dir:
    clear_temp()

    # Check if default directories for samples and saved songs exists, if not, create them:
    default_dirs()

    # Create objects:
    keys = Keypad()
    song_data = SongData()

    # Create serial_usb:
    serial_usb = serial.Serial('/dev/ttyUSB0', 31250)

    # Create audio files player in another process:
    queue_player = multiprocessing.Queue()
    proc_player = multiprocessing.Process(target=player_audiofiles, args=(queue_player,))
    proc_player.start()

    '''
    All of the song data are stored in song_data object. When song is loaded, 
    the object is loaded via pickle. List data_for_threads is created, so after loading new song data, 
    reference in that list to old song_data is replaced by new one. Threads in their main loop are checking, 
    if reference change, and if it changed, they are updating their reference to song_data object.
    '''
    data_for_threads = {
                        'song_data': song_data, 
                        'serial_usb': serial_usb, 
                        'queue_player': queue_player
                        }

    # Create thread for potentiometers:
    thread_pots = Thread(target=pots_operations, args=(data_for_threads,))
    thread_pots.start()

    # Create thread for note player:
    thread_player = Thread(target=player.main_loop, args=(data_for_threads,))
    thread_player.start()

    # Playlist Loop:
    playlist.main(keys, song_data, data_for_threads)

if __name__ == "__main__":
    main()
