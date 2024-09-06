from gui import gui_tracker
from gui import gui_warning_window
from libs.keypad import Keypad
from core.data_storage import DataStorage
from core.pick_file import getFilename
import os
import asyncio

#lambdas:
clear_screen = lambda: os.system("clear")


def createNewEmptyPattern():
	pattern = []
	for i in range(16):
		#Max 16 samples:
		pattern_for_single_sample = []
		for j in range(16):
			#16 quarter notes in pattern:
			pattern_for_single_sample.append([])
		pattern.append(pattern_for_single_sample)
	return pattern


def checkIfPatternIsEmpty(pattern):
	isEmpty = True
	for i in range(len(pattern)):
		for j in range(len(pattern[i])):
			if len(pattern[i][j]) == 2:
				isEmpty = False
	return isEmpty

	

def changeNote(operation, note_and_octave, tracker_cursor):
	notes_string_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	note_and_octave = note_and_octave.replace(" ", '')
	
	if operation == "semitone down":
		octave = note_and_octave[-1:]
		note = note_and_octave[:-1]
		note_index = notes_string_list.index(note)
		# if sound is eg C5 then switch to note B4, octave cannot be lower than 1:
		if note_index == 0 and int(octave) >= 2: 
			note = notes_string_list[len(notes_string_list) - 1]
			octave = str( int(octave) - 1 )
		# If note is eg C#5, then switch note to C5	
		else: 
			note_index -= 1
			note = notes_string_list[note_index]
		
		new_note = note + str(octave)
		
	if operation == "semitone up":	
			# Change note value up:
		if tracker_cursor[2] == 0:
			octave = note_and_octave[-1:]
			note = note_and_octave[:-1]
			note_index = notes_string_list.index(note)
			# if sound is eg B5 then switch to note C6, octave cannot be higher than 7:
			if note_index == len(notes_string_list) - 1 and int(octave) <= 7: 
				note = notes_string_list[0]
				octave = str( int(octave) + 1 )

			# If note is eg C#5, then switch note to C5	
			else: 
				note_index += 1
				note = notes_string_list[note_index]
			new_note = note + str(octave)
		
	return new_note

async def main(keys, data_storage, pattern_number):
	
	guitracker = lambda samples_list, this_pattern, pattern_number, song_name, selected_button, cursor: gui_tracker.main(list_of_samples = samples_list, 
								pattern = this_pattern, 
								is_playing = data_storage.get_data("is_playing"), 
								bpm_value = data_storage.get_data("bpm"), 
								swing_value = data_storage.get_data("swing"), 
								vol_value = data_storage.get_data("bvol"), 
								pattern_number = pattern_number,
								song_name = song_name,
								selected_button = selected_button, 
								cursor = cursor,
								playing_mode = data_storage.get_data("patternmode_is_song_playing"))

	guitrackerNoPrinting = lambda samples_list, this_pattern, pattern_number, song_name, selected_button, cursor: gui_tracker.main(list_of_samples = samples_list, 
									pattern = this_pattern, 
									is_playing = data_storage.get_data("is_playing"), 
									bpm_value = data_storage.get_data("bpm"), 
									swing_value = data_storage.get_data("swing"), 
									vol_value = data_storage.get_data("bvol"), 
									pattern_number = pattern_number,
									song_name = song_name,
									selected_button = selected_button, 
									cursor = cursor,
									print_on_screen = False,
									playing_mode = data_storage.get_data("patternmode_is_song_playing"))
	
	song_name = data_storage.get_data("song_name")

	volume_string_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
	tracker_cursor = [0, 0, 0]
	
	potentiometers_previous_values = [None, None, None]
	

	drums_patterns_order = data_storage.get_data("drums_patterns_order")
	# If pattern does not exist already, then create new empty pattern:
	if pattern_number not in drums_patterns_order:
		patterns = data_storage.get_data("drums_patterns")
		patterns.append(createNewEmptyPattern())
		
		drums_patterns_order = data_storage.get_data("drums_patterns_order")
		drums_patterns_order.append(pattern_number)
		
		data_storage.put_data("drums_patterns", patterns)
		data_storage.put_data("drums_patterns_order", drums_patterns_order)
		
		
	
	samples = data_storage.get_data("samples")
	pattern = data_storage.drumsPatternOperations("get pattern", pattern_number)

	
	while True:
		bpm = data_storage.get_data("bpm")
		swing = data_storage.get_data("swing")
		bvol = data_storage.get_data("bvol")
		
		if bpm != potentiometers_previous_values[0] or swing != potentiometers_previous_values[1] or bvol != potentiometers_previous_values[2]:
			potentiometers_previous_values[0] = bpm
			potentiometers_previous_values[1] = swing
			potentiometers_previous_values[2] = bvol
			clear_screen()
			guitracker(samples_list = samples, 
					   this_pattern = pattern, 
					   pattern_number = pattern_number, 
					   song_name = song_name, 
					   selected_button = None, 
					   cursor = tracker_cursor)
		
		
		#if tracker_cursor[0] == 0 and tracker_cursor[2] != 0 and len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0: tracker_cursor[2] = 0
		
		key = keys.check_keys()
		if key != '':
				
					
			# Escape key:
			if key == '1':
				patternIsEmpty = checkIfPatternIsEmpty(pattern)
				if patternIsEmpty:
						# Delete pattern from patterns list and pattern orders list:
						data_storage.drumsPatternOperations("delete_pattern", pattern_number)
				# exit to playlist:
				break

			if key == "*":
				is_playing = data_storage.get_data("is_playing")
				if is_playing:
					data_storage.put_data("is_playing", False)
				else:
					data_storage.put_data("is_playing", True)
					
			
			# Direction key - down:
			if key == '8':
				if tracker_cursor[1] + 1 <= 16:
					tracker_cursor[1] += 1
				else: tracker_cursor[1] = 0
			
			# Direction key - up:
			if key == '2':
				if tracker_cursor[1] - 1 >= 0:
					tracker_cursor[1] -= 1
					
				else: tracker_cursor[1] = 16
			
			# Direction key = right:
			if key == '6':
				# move to next sample
				if tracker_cursor[1] == 0:
					if tracker_cursor[0] + 1 < 16:
						tracker_cursor[0] += 1
					else:
						tracker_cursor[0] = 0
				
				else:
					# move jump to next note, if current field is empty, ommit volume subfield:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
						tracker_cursor[2] = 0
						if tracker_cursor[0] + 1 < 16:
							tracker_cursor[0] += 1
						else:
							tracker_cursor[0] = 0

					else:
						if tracker_cursor[2] == 1:
							tracker_cursor[2] = 0
							if tracker_cursor[0] + 1 < 16:
								tracker_cursor[0] += 1
							else:
								tracker_cursor[0] = 0

						elif tracker_cursor[2] == 0:
							tracker_cursor[2] = 1
							
			# Direction key = right:
			if key == '4':
				# move to next sample
				if tracker_cursor[1] == 0:
					if tracker_cursor[0] + 1 < 16:
						tracker_cursor[0] -= 1
					else:
						tracker_cursor[0] = 0
				
				else:
					# move jump to next note, if current field is empty, ommit volume subfield:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
						tracker_cursor[2] = 1
						if tracker_cursor[0] - 1 > -1:
							tracker_cursor[0] -= 1
						else:
							tracker_cursor[0] = 15

					else:
						if tracker_cursor[2] == 0:
							tracker_cursor[2] = 1
							if tracker_cursor[0] - 1 > -1:
								tracker_cursor[0] -= 1
							else:
								tracker_cursor[0] = 15

						elif tracker_cursor[2] == 1:
							tracker_cursor[2] = 0
								
			if key == '7':
				# if field on playlist is highlighted:
				if tracker_cursor[1] > 0:
					# Add note with volume:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ["C5", 'F']

					else:
						# Change note value down:
						if tracker_cursor[2] == 0:
							note_and_octave = pattern[tracker_cursor[0]][tracker_cursor[1]-1][tracker_cursor[2]]
							new_note = changeNote("semitone down", note_and_octave, tracker_cursor[:])
							pattern[tracker_cursor[0]][tracker_cursor[1]-1][tracker_cursor[2]] = new_note

						# Change note's volume value:
						if tracker_cursor[2] == 1:
							volume = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
							volume_index = volume_string_list.index(volume)
							if volume_index > 0:
								volume_index -= 1
								volume = volume_string_list[volume_index]
							pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = volume

					data_storage.put_data("drums_last_added_note", [pattern[tracker_cursor[0]][tracker_cursor[1]-1][0], 
								pattern[tracker_cursor[0]][tracker_cursor[1] - 1][1]])

					# update pattern in data storage:
					data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)
				
				else:
					# if sample highlighed on the screen, change volume of the sample:
					volumes = data_storage.get_data("samples_volume")
					if volumes[tracker_cursor[0]] - 1 >= 0:
						volumes[tracker_cursor[0]] -= 1
						data_storage.put_data("samples_volume", volumes)
				
				
			if key == '9':
				# if field on playlist is highlighted:
				if tracker_cursor[1] > 0:
					# Add note with volume:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
						#print(pattern)
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ["C5", 'F']
						#print(pattern)
						
					else:

						
						# semitone up:
						if tracker_cursor[2] == 0:
							note_and_octave = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
							new_note = changeNote("semitone up", note_and_octave, tracker_cursor[:])
							pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = new_note


						# Change note's volume value:
						elif tracker_cursor[2] == 1:
							print("doopa")
							volume = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
							volume_index = volume_string_list.index(volume)
							if volume_index < len(volume_string_list) - 1:
								volume_index += 1
								volume = volume_string_list[volume_index]
							pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = volume

					data_storage.put_data("drums_last_added_note", [pattern[tracker_cursor[0]][tracker_cursor[1] - 1][0], 
								pattern[tracker_cursor[0]][tracker_cursor[1] - 1][1]])

					# update pattern in data storage:
					data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)	

				else:
					# if sample highlighed on the screen, change volume of the sample:
					volumes = data_storage.get_data("samples_volume")
					if volumes[tracker_cursor[0]] + 1 <= 10:
						volumes[tracker_cursor[0]] += 1
						data_storage.put_data("samples_volume", volumes)
	
							
			# Insert key:
			if key == '5':
				# If cursor is on samples level, insert sample / change sample to other one:
				if tracker_cursor[1] == 0:
					# Choose sample from disk with getFilename function and get path to choosen sample:
					sample_path = getFilename("sample", keys)
					if sample_path is not None:
						samples[tracker_cursor[0]] = sample_path
						data_storage.put_data("samples", samples)
					
				# if cursor is on playlist:
				elif tracker_cursor[1] > 0:
					# if note is empty, add last added note:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = data_storage.get_data("drums_last_added_note")
					# if field for note is not empty, delete note:
					else:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = []
					# update pattern in data storage:
					data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)
	
			#clear single track:
			if key == "0":
				ok_selected = False
				screen_matrix = guitracker(samples_list = samples, 
							   this_pattern = pattern, 
							   pattern_number = pattern_number, 
							   song_name = song_name, 
							   selected_button = None, 
							   cursor = tracker_cursor)
				clear_screen()
				gui_warning_window.main(screen_matrix, ok_selected, "clear track")
				
				while True:			
					key = keys.check_keys()
					if key != '':
						if key == '1':
							break
						
						if key == '4' and ok_selected == False: ok_selected = True
						if key == '6' and ok_selected == True: ok_selected = False
						
						if key == '5':
							if ok_selected:
								for i in range(16):
									pattern[tracker_cursor[0]][i] = []
								break
							
							else: break	
						
						clear_screen()
						gui_warning_window.main(screen_matrix, ok_selected, "clear track")
						
						
			# Change playing mode from looping pattern to playing whole song:
			if key == "3":
				is_song_playing = data_storage.get_data("patternmode_is_song_playing")
				if is_song_playing:
					is_song_playing = False
				else:
					is_song_playing = True

				data_storage.put_data("patternmode_is_song_playing", is_song_playing)	
				
				
			# Pattern Menu:
			if key == "#":
				menu_cursor = [0, 0]
				selected = 0
				
				clear_screen()
				guitracker(samples_list = samples, 
					   this_pattern = pattern, 
					   pattern_number = pattern_number, 
					   song_name = song_name, 
					   selected_button = selected, 
					   cursor = tracker_cursor)

				
				while True:
					key = keys.check_keys()
					if key != '':
						# Menu up
						if key == "2":
							if menu_cursor[0] > 0:
								menu_cursor[0] -= 1
						
						#Menu down
						if key == "8":
							if menu_cursor[0] < 2:
								menu_cursor[0] += 1
						
						#menu left
						if key == "4":
							if menu_cursor[1] == 1:
								menu_cursor[1] = 0
						
						#menu right	
						if key == "6":
							if menu_cursor[1] == 0:
								menu_cursor[1] = 1		
						
						#escape button - exit menu, go back to playlist:
						if key == "1" or key == "#":
							break
						
		
						
						# [insert] key - accept:
						if key == "5":
							# toggling patterns:
							if selected < 3:
								new_pattern_number = pattern_number
								key = ''
								
								if pattern_number - 1 > 0 or pattern_number + 1 < 999:
									# update pattern in data storage:
									data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)
									if selected == 0:
										new_pattern_number = pattern_number - 1
									elif selected == 1:
										new_pattern_number = pattern_number + 1
									elif selected == 2:
										drums_patterns_order = data_storage.get_data("drums_patterns_order")
										for i in range(998):
											if i + 1 not in drums_patterns_order:
												# Update pattern order list:
												new_pattern_number = i + 1
												drums_patterns_order.append(new_pattern_number)
												data_storage.put_data("drums_patterns_order", drums_patterns_order)

												#clone pattern to list of patterns
												patterns = data_storage.get_data("drums_patterns")
												patterns.append(pattern)
												data_storage.put_data("drums_patterns", patterns)
												break		
								return new_pattern_number
							
							#clear pattern:
							elif selected == 3:
								warning_windows_selected_ok = False
								clear_screen()
								screen_matrix = guitrackerNoPrinting(samples_list = samples, 
														   this_pattern = pattern, 
														   pattern_number = pattern_number, 
														   song_name = song_name, 
														   selected_button = selected, 
														   cursor = tracker_cursor)
								gui_warning_window.main(screen_matrix, warning_windows_selected_ok, "clear song")
								
								while True:
									key = keys.check_keys()
									if key != "":
										if key == "4" and warning_windows_selected_ok == False:
											warning_windows_selected_ok = True
										elif key == "6" and warning_windows_selected_ok == True:
											warning_windows_selected_ok = False

										if key == "5":
											if warning_windows_selected_ok:
												pattern = createNewEmptyPattern()
												data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)
												break
											else:
												break
												
										if key == "1":
												break
										clear_screen()
										gui_warning_window.main(screen_matrix, warning_windows_selected_ok, "clear song")

						
						if menu_cursor[0] == 0:
							selected = menu_cursor[1]
			

						elif menu_cursor[0] == 1:
							selected = 2
							

						elif menu_cursor[0] == 2:
							selected = 3
						
						
						clear_screen()
						guitracker(samples_list = samples, 
						   this_pattern = pattern, 
						   pattern_number = pattern_number, 
						   song_name = song_name, 
						   selected_button = selected, 
						   cursor = tracker_cursor)	
						
							
			
			# if key pressed, update displayed gui:
			clear_screen()
			guitracker(samples_list = samples, 
					   this_pattern = pattern, 
					   pattern_number = pattern_number, 
					   song_name = song_name, 
					   selected_button = None, 
					   cursor = tracker_cursor[:])
		await asyncio.sleep(0.1)
			#print(tracker_cursor)
			#print(pattern[tracker_cursor[0]][tracker_cursor[1]-1])
					
if __name__ == "__main__":
	keys = Keypad()
	data_storage = DataStorage()
	main(keys, data_storage, 1)
