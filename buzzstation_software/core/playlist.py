from libs.keypad import Keypad
from gui import gui_playlist, gui_warning_window
from .data_storage import DataStorage
import time
import os
import copy
import pickle
from . import tracker
from . import pianoroll
from . import pick_file
from . import pick_midi_instrument

# Lambdas:
clear_screen = lambda: os.system("clear")
GUIplaylist = lambda gui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname: gui_playlist.main(
								list_of_instruments = list_of_instruments,
								bpm_value = bpm,
								swing_value = swing,
								vol_value = bvol,
								playlist = playlist,
								gui_cursor = gui_cursor,
								menu_selected = menu_selected,
								songname = songname
								)

GUIgetScreenMatrix = lambda  gui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname: gui_playlist.main(
								list_of_instruments = list_of_instruments,
								bpm_value = bpm,
								swing_value = swing,
								vol_value = bvol,
								playlist = playlist,
								gui_cursor = gui_cursor,
								menu_selected = menu_selected,
								songname = songname,
								printgui = False
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
		
def playlist_loop(keys, data_storage):
	
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
						bvol = bvol,
						songname = data_storage.get_data("song_name")
					   )
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
					if playlist_cursor[0] < 15:
						playlist_cursor[1] += 1

				
				#create list with 
				if playlist_cursor[1] > len(song_playlist[0]):
					for i in range(len(song_playlist)):
						for j in range(16):
							song_playlist[i].append(" ")
							
				
			if key == '4':
				# Move left in matrix:
				if playlist_cursor[0] > 0: 
					playlist_cursor[0] -= 1
				elif playlist_cursor[0] == 0:
					# jump to firs from right added instrument:
					playlist_cursor[0] = len(song_playlist) - 1
					
			# Edit selected pattern:
			if key == '3':
				key == ''
				if playlist_cursor[1]-1 < 0:
					pattern_number_for_tracker = None
				else:
					pattern_number_for_tracker = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
				
				while True:
					# Select new midi instrument for midi output:
					if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
						midi_output = data_storage.get_data("playlist_list_of_instruments")[playlist_cursor[0]]
						if midi_output != "Empty":
							midi_instruments = data_storage.get_data("playlist_list_of_midi_assigned")
							midi_instrument = midi_instruments[midi_output][0]
							choosen_instrument = pick_midi_instrument.main(keys, midi_output, midi_instrument)

							if choosen_instrument is not None:
								midi_instruments[midi_output] = choosen_instrument
								data_storage.put_data("playlist_list_of_midi_assigned", midi_instruments)
							break
							
					if pattern_number_for_tracker is None or pattern_number_for_tracker == ' ':
							break
					
					if playlist_cursor[0] == 0:
						pattern_number_for_tracker = tracker.main(keys, data_storage, pattern_number_for_tracker)
					elif playlist_cursor[0] > 0 and playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						pattern_number_for_tracker = pianoroll.main(keypad = keys, 
																		  data_storage = data_storage,
																		  pattern_number = pattern_number_for_tracker,
																		  midi_and_channel = playlist_list_of_instruments[playlist_cursor[0]],
																		  track = playlist_cursor[0] - 1)
						

			
			
			if key == '6':
				# move right in matrix
				# Wake up, Neo
				
				if playlist_cursor[0] + 1 == len(playlist_list_of_instruments):
					# if cursor point to instrument that is not in playlist_list_of_instruments, add more empty to not exceed list length:
					for i in range(8): playlist_list_of_instruments.append("Empty")

				if playlist_cursor[0] == 15:
					playlist_cursor[0] = 0
						
				# Move cursor to next Empty instrument only when instrument on which cursor points to is not empty:
				elif playlist_list_of_instruments[playlist_cursor[0]] != "Empty" and playlist_cursor[1] == 0:
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

			
			# clear track key:
			if key == '0':
				screen_matrix = GUIgetScreenMatrix(gui_cursor = playlist_cursor[:], 
									playlist = song_playlist, 
									menu_selected = None, 
									list_of_instruments = playlist_list_of_instruments, 
									bpm = bpm, 
									swing = swing, 
									bvol = bvol,
									songname = data_storage.get_data("song_name")
								   )


				ok_selected = False
				clear_screen()
				gui_warning_window.main(screen_matrix, ok_selected, "clear song")
				
				while True:
					key = keys.check_keys()
					if key != "":
						if key == "4":
							ok_selected = True
						
						if key == "6":
							ok_selected == False
						
						if key == "1": break
						
						if key == "5":
							key = ""
							if ok_selected:
								for i in range(len(song_playlist[playlist_cursor[0]])):
									song_playlist[playlist_cursor[0]][i] = " " 
								break
							else:
								break
							
						clear_screen()	
						gui_warning_window.main(screen_matrix, ok_selected, "clear song")	
						
					

						
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

			
			if key == '#':
				# Enter menu to save or load song:
				selected = 0
				menu_cursor = [0, 0]
				clear_screen()
				GUIplaylist(gui_cursor = playlist_cursor[:], 
							playlist = song_playlist, 
							menu_selected = selected, 
							list_of_instruments = playlist_list_of_instruments, 
							bpm = bpm, 
							swing = swing, 
							bvol = bvol,
							songname = data_storage.get_data("song_name")
						   )
				
				while True:
					key = keys.check_keys()
					if key != "":
						previous_selected = selected
						if key == '4':
							if menu_cursor[1] == 1:
								menu_cursor[1] = 0

						if key == '6':
							if menu_cursor[1] == 0:
								menu_cursor[1] = 1

						if key == '2':
							if menu_cursor[0] - 1 > -1:
								menu_cursor[0] -= 1

						if key == '8':
							if menu_cursor[0] + 1 < 4:
								menu_cursor[0] += 1
														
						if key == '1' or key == "#":
							# Exit menu:
							break		

						if menu_cursor[0] == 0:
							if menu_cursor[1] == 0:
								selected = 0
							else:
								selected = 1
								
						if menu_cursor[0] == 1:
								selected = 2
								
						if menu_cursor[0] == 2:
								selected = 3
								
							
						if previous_selected != selected:
							clear_screen()
							GUIplaylist(gui_cursor = playlist_cursor[:], 
										playlist = song_playlist, 
										menu_selected = selected, 
										list_of_instruments = playlist_list_of_instruments, 
										bpm = bpm, 
										swing = swing, 
										bvol = bvol,
										songname = data_storage.get_data("song_name")
										)
							previous_selected = selected 
	
						
						if key == '5':
							screen_matrix = GUIgetScreenMatrix(gui_cursor = playlist_cursor[:], 
																playlist = song_playlist, 
																menu_selected = None, 
																list_of_instruments = playlist_list_of_instruments, 
																bpm = bpm, 
																swing = swing, 
																bvol = bvol,
																songname = data_storage.get_data("song_name")
															   )
					
							# Accept choice:
							if selected == 0:
								# Save song:
								path_to_file = pick_file.getFilename("save song", keys)
								should_save_song = True
								
								# Check if file already exist, then ask user, if he wants to overwrite it:
								if path_to_file is not None:
									if os.path.isfile(path_to_file):
										ok_selected = False
										screen_matrix = []
										line = []
										for i in range(64):
											line.append(" ")
										for i in range(17):
											screen_matrix.append(line[:])
									
											
										for i in range(len(path_to_file)):
											screen_matrix[0][i] = path_to_file[i]
											
										gui_warning_window.main(screen_matrix, ok_selected, "overwrite song")
									
										while True:
											key = keys.check_keys()
											if key != "":
												if key == "4": ok_selected = True
												if key == "6": 	ok_selected = False
												if key == "5":
													if not ok_selected: should_save_song = False
													else:
														os.remove(path_to_file)
														break
												clear_screen()
												gui_warning_window.main(screen_matrix, ok_selected, "overwrite song")
										
								if should_save_song and path_to_file is not None:
									with open(path_to_file, 'wb') as file_btp:
										pickle.dump(data_storage, file_btp)
										
								key = ""
								clear_screen()
								GUIplaylist(gui_cursor = playlist_cursor[:], 
											playlist = song_playlist, 
											menu_selected = selected, 
											list_of_instruments = playlist_list_of_instruments, 
											bpm = bpm, 
											swing = swing, 
											bvol = bvol,
											songname = data_storage.get_data("song_name")
											)
								break
							
							elif selected > 0:
								if selected == 1:
									warning_text = "load song"
								if selected == 2:
									warning_text = "new song"
								if selected == 3:
									warning_text = "clear all tracks"
								
								ok_selected = False
								clear_screen()
								gui_warning_window.main(screen_matrix, ok_selected, warning_text)
								
								while True:
									key = keys.check_keys()
									if key != "":
										if key == "4":
											ok_selected = True

										if key == "6":
											ok_selected = False

										if key == "1": break

										if key == "5":
											if ok_selected:
												if selected == 1:
													# Load Song
													path_to_file = pick_file.getFilename("load song", keys)
													if path_to_file is not None:
														with open(path_to_file, 'rb') as file_btp:
															data_storage = pickle.load(file_btp)
															song_playlist = data_storage.get_data("song_playlist")
															playlist_list_of_instruments = data_storage.get_data("playlist_list_of_instruments")
												
												elif selected == 2:
													#new song: clear all previous data
													data_storage = DataStorage()
													playlist_cursor = [0, 0]
													createEmptySongPlaylist(data_storage)
													song_playlist = data_storage.get_data("song_playlist")
													playlist_list_of_instruments = data_storage.get_data("playlist_list_of_instruments")
												
												elif selected == 3:
													# Clear entire playlist:
													song_playlist = data_storage.get_data("song_playlist")

													track_for_instrument = []
													for i in range(16):
														track_for_instrument.append(" ")

													for i in range(len(song_playlist)):
														song_playlist[i] = track_for_instrument[:]
													data_storage.put_data("song_playlist", song_playlist)
												key = ""
												clear_screen()
												GUIplaylist(gui_cursor = playlist_cursor[:], 
															playlist = song_playlist, 
															menu_selected = selected, 
															list_of_instruments = playlist_list_of_instruments, 
															bpm = bpm, 
															swing = swing, 
															bvol = bvol,
															songname = data_storage.get_data("song_name")
															)
												break
			
										clear_screen()
										gui_warning_window.main(screen_matrix, ok_selected, warning_text)	
					
							break
							

	

						

			
			if key == '*':
				playSong()
				
			if key == '5':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					# Assign new midi output port to an empty instrument slot:
					if playlist_list_of_instruments[playlist_cursor[0]] == "Empty":
						playlist_list_of_instruments[playlist_cursor[0]] = "M1c1"
						createEmptySongPlaylist(data_storage)
						song_playlist = data_storage.get_data("song_playlist")

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
						bvol = bvol,
						songname = data_storage.get_data("song_name")
					   )	
		
		# Update values in data storage:
		data_storage.put_data("playlist_cursor", playlist_cursor)
		data_storage.put_data("song_playlist", song_playlist)
		data_storage.put_data("playlist_list_of_instruments", playlist_list_of_instruments)


if __name__ == "__main__":
	playlist_loop()
