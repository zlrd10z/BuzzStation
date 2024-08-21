from libs.keypad import Keypad
from gui import gui_playlist
from .potentiometers_operations import potentiometersOperations
from .data_storage import DataStorage
import time
import os
import copy
import asyncio

# Lambdas:
clear_screen = lambda: os.system("clear")
GUIplaylist = lambda gui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol: gui_playlist.main(
								list_of_instruments = list_of_instruments,
								bpm_value = bpm,
								swing_value = swing,
								vol_value = bvol,
								playlist = playlist,
								gui_cursor = gui_cursor,
								menu_selected = menu_selected,
								)


def saveSong():
	print("song saved")
	# testing purpose:
	#while True: pass

def loadSong():
	print("song loaded")
	# testing purposez
	#while True: pass
	
def playSong():
	pass

def createEmptySongPlaylist(data_storage):
	song_playlist = data_storage.get_data("song_playlist")
	track_for_instrument = []
	for i in range(16):
		track_for_instrument.append(" ")
	song_playlist.append(track_for_instrument)
	data_storage.put_data("song_playlist", song_playlist)

#If there is nothing saved after the first 16 fields, delete after 16 fields the rest of the playlist consisting of empty characters to save memory:
def shortenPlaylistIfPossible(playlist):
	# Check if playlist can be shorten:
	for i in range(len(playlist)):
		can_be_shorten = True
		
		for j in range(16):
			if playlist[i][len(playlist) - 1 - j] != " ":
				can_be_shorten = False
		
		# Cut last 16 empty fields:
		if can_be_shorten:
			for i in range(len(playlist)):
				playlist[i] = playlist[i][:-16]
				
		return playlist
		
async def playlist_loop(keys, data_storage):

	
	createEmptySongPlaylist(data_storage)
	previous_printed_values = [0, 0, 0]
	
	# Playlist loop:
	while True:
		# Get lists from data storage:
		playlist_cursor = data_storage.get_data("playlist_cursor")
		song_playlist = data_storage.get_data("song_playlist")
		playlist_list_of_instruments = data_storage.get_data("playlist_list_of_instruments")
		
		# Get potentiometers transformed data from data storage object:
		bpm = data_storage.get_data("bpm")
		swing = data_storage.get_data("swing")
		bvol = data_storage.get_data("bvol")
	
		# Update screen, if any value from potentiometers has changed:
		if previous_printed_values[0] != bpm or previous_printed_values[1] != swing or previous_printed_values[2] != bvol:
			clear_screen()
			GUIplaylist(gui_cursor = playlist_cursor[:], 
						playlist = song_playlist, 
						menu_selected = None, 
						list_of_instruments = playlist_list_of_instruments, 
						bpm = bpm, 
						swing = swing, 
						bvol = bvol)
			previous_printed_values[0] = bpm
			previous_printed_values[1] = swing	
			previous_printed_values[2] = bvol
		
		# Keys 2 and 8 are up and down keys, keys 4 and 6 are left and right keys
		# Get key from keypad:	
		key = keys.check_keys()
		if key != "":
			if key == '2':
				# Move UP in matrix:
				if playlist_cursor[1] > 0:
					playlist_cursor[1] -=  1
					if playlist_cursor[1] < (len(song_playlist[0]) -1) - 16:
						song_playlist = shortenPlaylistIfPossible(song_playlist)
				
			if key == '8':
				# Move DOWN im matrix:
				if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
					playlist_cursor[1] += 1
				if playlist_cursor[1] > len(song_playlist[0]):
					for i in range(len(song_playlist)):
						for j in range(16):
							song_playlist[i].append(" ")
							
				
			if key == '4':
				# Move left in matrix:
				if playlist_cursor[0] > 0: 
					playlist_cursor[0] -= 1
					

					
			if key == '6':
				# move right in matrix
				# Wake up, Neo
				
				if playlist_cursor[0] + 1 == len(playlist_list_of_instruments):
					# if cursor point to instrument that is not in playlist_list_of_instruments, add more empty to not exceed list length:
					for i in range(8): playlist_list_of_instruments.append("Empty")

				# Move cursor to next Empty instrument only when instrument on which cursor points to is not empty:
				if playlist_list_of_instruments[playlist_cursor[0]] != "Empty" and playlist_cursor[1] == 0:
					playlist_cursor[0] += 1
				
				# Move cursor on playlist to next intrument, only if it's not Empty:
				elif playlist_list_of_instruments[playlist_cursor[0] + 1] != "Empty" and playlist_cursor[1] != 0:
					playlist_cursor[0] += 1
					
			if key == '7':
				# Toggle down midi instrument channel:
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) - 1 == 0:
							channel = 16
						else:
							channel = int(midi_instrument[3:]) - 1
						midi_instrument = midi_instrument[:3] + str(channel)
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
						
						
				# Change selected pattern to previous pattern (eg. from pattern 2 to pattern 1):
				elif playlist_cursor[1] != 0:
					# Remove pattern from a field:
					if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] == '1':
						song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = ' '
	
					# toggle down pattern:	
					else:
						if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] != ' ':
							patt_number = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
							patt_number = int(patt_number) - 1
							song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = patt_number
							data_storage.put_data("last_added_pattern_numer", patt_number)

						
						
			if key == '9':
				# Toggle up midi instrument channel:
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) + 1 == 17:
							channel = 1
						else:
							channel = int(midi_instrument[3:]) + 1
						midi_instrument = midi_instrument[:3] + str(channel)
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
						
				# Change selected pattern to previous pattern (eg. from pattern 1 to pattern 2):
				elif playlist_cursor[1] != 0:
					# Add pattern to an empty field:
					if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] == ' ':
						song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = '1'
	
					# toggle down pattern:	
					else:
						if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] != ' ':
							patt_number = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
							patt_number = int(patt_number) + 1
							song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = patt_number
							data_storage.put_data("last_added_pattern_numer", patt_number)

			
			if key == '3':
				# Enter menu to save or load song:
				selected = 0
				clear_screen()
				GUIplaylist(gui_cursor = playlist_cursor[:], 
							playlist = song_playlist, 
							menu_selected = selected, 
							list_of_instruments = playlist_list_of_instruments, 
							bpm = bpm, 
							swing = swing, 
							bvol = bvol)
				
				while True:
					key = keys.check_keys()
					if key != "":
						if key == '4' or key == '6':
							new_selected = selected
							if key == '4':
								if selected == 1:
									new_selected = 0

							if key == '6':
								if selected == 0:
									new_selected = 1
							
							if new_selected != selected:
								clear_screen()
								GUIplaylist(gui_cursor = playlist_cursor[:], 
								playlist = song_playlist, 
								menu_selected = selected, 
								list_of_instruments = playlist_list_of_instruments, 
								bpm = bpm, 
								swing = swing, 
								bvol = bvol)
								selected = new_selected
	
						
						if key == '5':
							# Accept choice:
							if selected == 0:
								saveSong()
							else:
								loadSong()
							break
								
						if key == '1':
							# Exit menu:
							break
						

			
			if key == '*':
				playSong()
				
			if key == '5':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					# Assign new midi output port to an empty instrument slot:
					if playlist_list_of_instruments[playlist_cursor[0]] == "Empty":
						playlist_list_of_instruments[playlist_cursor[0]] = "M1c1"
						createEmptySongPlaylist(data_storage)

					# Change midi output port, if instrument slot is not empty:
					elif playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						midi_channel = midi_instrument[2:]
						midi_output = int(midi_instrument[1])

						if midi_output == 3:
							midi_output = 1
						else:
							midi_output += 1
						playlist_list_of_instruments[playlist_cursor[0]] = 'M' + str(midi_output) + midi_channel
					
				# Add of delete pattern on selected field:
				elif playlist_cursor[1]  != 0:
					# Add last picked pattern (pattern picking with buttons [7] and [9]:
					if song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] == ' ':
						song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = data_storage.get_data("last_added_pattern_numer")
						
					# delete pattern:	
					else:
						song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = ' '
						
			clear_screen()
			GUIplaylist(gui_cursor = playlist_cursor[:], 
						playlist = song_playlist, 
						menu_selected = None, 
						list_of_instruments = playlist_list_of_instruments, 
						bpm = bpm, 
						swing = swing, 
						bvol = bvol)	
		
		# Update values in data storage:
		data_storage.put_data("playlist_cursor", playlist_cursor)
		data_storage.put_data("song_playlist", song_playlist)
		data_storage.put_data("playlist_list_of_instruments", playlist_list_of_instruments)
		await asyncio.sleep(0.1)

if __name__ == "__main__":
	playlist_loop()
