from threading import Thread
from libs.keypad import Keypad
from core.data_storage import DataStorage
from core.playlist import playlist_loop
from core.potentiometers_operations import pots_operations
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
	data_storage = DataStorage()

	#Create thread for potentiometers:
	thread_pots = Thread(target=pots_operations, args=[data_storage])
	thread_pots.start()
	
	#main loop:
	playlist_loop(keys, data_storage)


if __name__ == "__main__":
	main()
