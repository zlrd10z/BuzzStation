from threading import Thread
from libs.keypad import Keypad
from gui import gui_playlist
from core.data_storage import DataStorage
from core.playlist import playlist_loop
from core.potentiometers_operations import potentiometersOperations
import time


def main():
	# Create objects:
	keys = Keypad()
	data_storage = DataStorage()

	#Create thread for potentiometers:
	thread_pots = Thread(target=potentiometersOperations, args=[data_storage])
	thread_pots.start()
	
	#main loop:
	print("123")
	playlist_loop(keys, data_storage)

	#thread_playlist = Thread(target=playlist_loop, args=[keys,data_storage])
	#thread_playlist.run()

if __name__ == "__main__":
	main()
