from threading import Thread
import multiprocessing
from libs.keypad import Keypad
from core.song_data import SongData
from core import playlist
from core.potentiometers_operations import pots_operations
from core.midi_and_sync.midi_process import midi_sender
import time
import os


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
    # Create another process for midi processing:
    queue_midi = multiprocessing.Queue
    proc_midi = multiprocessing.Process(target=midi_sender, args=(queue_midi,))
    proc_midi.start()
    song_data.put_data('queue_midi', queue_midi)
    #Create thread for potentiometers:
    thread_pots = Thread(target=pots_operations, args=[song_data])
    thread_pots.start()
    #main loop:
    playlist.main(keys, song_data)

if __name__ == "__main__":
    main()
