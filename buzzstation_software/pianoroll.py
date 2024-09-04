from gui import gui_warning_window
from gui import gui_pianoroll
from libs.keypad import Keypad
from core.data_storage import DataStorage

#=========================================================================================
# Lambdas:
printGui = lambda pattern_number, midi_and_channel, selected_note, selected_beat, pattern, selected_menu_button: gui_pianoroll.main(bpm_value = data_storage.get_data("bpm"), 
																																	  swing_value = data_storage.get_data("swing"), 
																																	  pattern_number = pattern_number, 
																																	  playing_mode = data_storage.get_data("patternmode_is_song_playing"), 
																																	  playing = data_storage.get_data("is_playing"), 
																																	  midi_output_and_channel = midi_and_channel, 
																																	  selected_note = selected_note, 
																																	  selecteded_beat = selected_beat, 
																																	  pattern = pattern, 
																																	  selected_menu_button=selected_menu_button,
																																	  print_gui = True
																																 	)	

getScreenMatrix = lambda pattern_number, midi_and_channel, selected_note, selected_beat, pattern, selected_menu_button: gui_pianoroll.main(bpm_value = data_storage.get_data("bpm"), 
																																		  swing_value = data_storage.get_data("swing"), 
																																		  pattern_number = pattern_number, 
																																		  playing_mode = data_storage.get_data("patternmode_is_song_playing"), 
																																		  playing = data_storage.get_data("is_playing"), 
																																		  midi_output_and_channel = midi_and_channel, 
																																		  selected_note = selected_note, 
																																		  selecteded_beat = selected_beat, 
																																		  pattern = pattern, 
																																		  selected_menu_button=selected_menu_button,
																																		  print_gui = False
																																		)	

printGuiEditNoteLength = lambda pattern_number, midi_and_channel, selected_note, selected_beat, pattern, selected_menu_button: gui_pianoroll.main(bpm_value = data_storage.get_data("bpm"), 
																																				  swing_value = data_storage.get_data("swing"), 
																																				  pattern_number = pattern_number, 
																																				  playing_mode = data_storage.get_data("patternmode_is_song_playing"), 
																																				  playing = data_storage.get_data("is_playing"), 
																																				  midi_output_and_channel = midi_and_channel, 
																																				  selected_note = selected_note, 
																																				  selecteded_beat = selected_beat, 
																																				  pattern = pattern, 
																																				  selected_menu_button=selected_menu_button,
																																				  print_gui = True,
																																				  note_length_edit = True
																																 				)	


def createEmptyPattern():
	pattern = []
	for i in range(16):
		l = []
		pattern.append(l)
	#                  [note, note length, volume]
	#    pattern[0].append(["C#5", 1, 8])

	return pattern


def main(keypad, data_storage, pattern_number, midi_and_channel, track):
		
	
	notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	selected_note_and_octave = "C5"
	selected_beat = 0
	
	
	# Check is this pattern exist or this is new pattern:
	pianoroll_patterns_order = data_storage.get_data("pianoroll_patterns_order")
	if pattern_number in pianoroll_patterns_order[track]:
		pattern = data_storage.pianorollPatternOperations("get pattern", track, pattern_number)
		
	else:
		#create new pattern:
		pianoroll_patterns_order[track].append(pattern_number)
		pattern = createEmptyPattern()
		data_storage.pianorollPatternOperations("put pattern", track, pattern_number, pattern)
		data_storage.put_data("pianoroll_patterns_order", pianoroll_patterns_order)
	
	previous_values = [None, None]
			
	while True:
		if data_storage.get_data("bpm") != previous_values[0] or data_storage.get_data("swing") != previous_values[1]:
			previous_values[0] = data_storage.get_data("bpm") 
			previous_values[1] = data_storage.get_data("swing") 
			printGui(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = None)
		
		key = keypad.check_keys()
		if key != "":

			# Direction key - left:
			if key == "4":
				if selected_beat > 0:
					selected_beat -= 1
				else:
					selected_beat = 15

			# Direction key - right:
			if key == "6":
				if selected_beat < 15:
					selected_beat += 1
				else:
					selected_beat = 0

			# Direction key - up:
			if key == "2":
				note = selected_note_and_octave[:-1]
				octave = selected_note_and_octave[-1]

				index = notes.index(note)
				if index + 1 < len(notes):
					note = notes[index + 1]

				else:
					if int(octave) < 8:
						note = notes[0]
						octave = int(octave) + 1

				selected_note_and_octave = note + str(octave)

			# Direction key - down:
			if key == "8":
				note = selected_note_and_octave[:-1]
				octave = selected_note_and_octave[-1]

				index = notes.index(note)
				if index > 0:
					note = notes[index - 1]

				else:
					if int(octave) > 2:
						note = notes[-1]
						octave = int(octave) - 1

				selected_note_and_octave = note + str(octave)	

			# Escape key:
			if key == "1":
				break
			#print(selected_note_and_octave, selected_beat)	
		
			
			# Insert key:
			if key == "5":
				already_exists = False
				index = None
				
				#check if note not exist already on selected beat:
				if len(pattern[selected_beat]) > 0:
					for i in range(len(pattern[selected_beat])):
						if pattern[selected_beat][i][0] == selected_note_and_octave:
							already_exists = True
							index = i
							break
				
				if not already_exists:
					pattern[selected_beat].append([selected_note_and_octave, 1, 8])
				
				elif already_exists:
					pattern[selected_beat].pop(index)

				data_storage.pianorollPatternOperations("update pattern", pattern_number, track, pattern)
					
				print(pattern[selected_beat])
		
			# edit length key:
			if key == "3":
				if len(pattern[selected_beat]) > 0:
					for i in range(len(pattern[selected_beat])):
						if selected_note_and_octave == pattern[selected_beat][i][0]:
							printGuiEditNoteLength(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = None)
							while True:
								key = keypad.check_keys()
								if key != "":
									if key == "1" or key == "3" or key == "5": 
										key = ""
										break
									
									elif key == "7" or key == "4":
										if pattern[selected_beat][i][1] > 1:
 												pattern[selected_beat][i][1]  -= 1
									
									elif key == "9" or key == "6": 
										if 16 - selected_beat > pattern[selected_beat][i][1]:
											# check if there is no note behind this note:
											if len(pattern[selected_beat + pattern[selected_beat][i][1]]) > 0:
												same_note_exists_one_quarter_behind = False
												for i in range(len(pattern[selected_beat + pattern[selected_beat][i][1]])):
													if pattern[selected_beat + pattern[selected_beat][i][1]][i][0] == selected_note_and_octave:
														same_note_exists_one_quarter_behind = True
														break
												
												if same_note_exists_one_quarter_behind == False: pattern[selected_beat][i][1]  += 1
												
														
													
											else:
												pattern[selected_beat][i][1] += 1
										
									data_storage.pianorollPatternOperations("update pattern", pattern_number, track, pattern)
									printGuiEditNoteLength(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = None)
							break
			# clear key:
			if key == "0":
				is_ok_selected = False
				screen_matrix = getScreenMatrix(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = 15)
				gui_warning_window.main(screen_matrix, is_ok_selected, "clear pattern")
				
				while True:
					key = keypad.check_keys()
					if key != "":
						# direction key - right
						if key == "6" and is_ok_selected:
							is_ok_selected = False
						# direction key = 	
						if key == "4" and is_ok_selected == False:
							is_ok_selected = True
				
						if key == "5":
							key = ''
							if is_ok_selected:
								pattern = createEmptyPattern()
								data_storage.pianorollPatternOperations("update pattern", pattern_number, track, pattern)
								break
							else:
								break
						
						if key == "1": break
						gui_warning_window.main(screen_matrix, is_ok_selected, "clear pattern")	
							
			#print(selected_note_and_octave)
			
			# volume up note:
			if key == "9":
				if len(pattern[selected_beat]) > 0:
					for i in range(len(pattern[selected_beat])):
						if pattern[selected_beat][i][0] == selected_note_and_octave:
							if pattern[selected_beat][i][2] < 8:
								pattern[selected_beat][i][2] += 1
								data_storage.pianorollPatternOperations("update pattern", pattern_number, track, pattern)
			# volume up note:
			if key == "7":
				if len(pattern[selected_beat]) > 0:
					for i in range(len(pattern[selected_beat])):
						if pattern[selected_beat][i][0] == selected_note_and_octave:
							if pattern[selected_beat][i][2] > 1:
								pattern[selected_beat][i][2] -= 1
								data_storage.pianorollPatternOperations("update pattern", pattern_number, track, pattern)
			# Menu key:
			if key == "#":
				menu_selected_button = 0
				printGui(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = menu_selected_button)
				
				while True:
					key = keypad.check_keys()
					if key != "":
						if key == '1' or key == "#":
							break

						# direction key - rigth:
						if key == '6':
							if menu_selected_button < 3:
								menu_selected_button += 1

						# direction key - left:
						if key == '4':
							if menu_selected_button > 0:
								menu_selected_button -= 1

						# accept key:
						if key == '5':
							if menu_selected_button != 1:
								# previous pattern:
								if menu_selected_button == 0:
									pattern_number -= 1
								# next pattern:
								elif menu_selected_button == 3:
									pattern_number += 1
								# clone pattern:
								elif menu_selected_button == 2:
									cloned_pattern_number = None
									pianoroll_patterns_order = data_storage.get_data("pianoroll_patterns_order", track)
									for i in range(999):
										if i not in pianoroll_patterns_order:
											cloned_pattern_number = i
											break

									if cloned_pattern_number is not None:
										pianoroll_patterns_order.append(cloned_pattern_number)
										data_storage.pianorollPatternOperations("put pattern", track, pattern_number, pattern[:])
										data_storage.put_data("pianoroll_patterns_order", pianoroll_patterns_order)
										pattern_number = cloned_pattern_number

								return pattern_number

							if menu_selected_button == 1:
								is_song_playing = data_storage.get_data("patternmode_is_song_playing")

								if is_song_playing: is_song_playing = False
								else: is_song_playing = True

								data_storage.put_data("patternmode_is_song_playing", is_song_playing)
								printGui(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = menu_selected_button)
								
						printGui(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = menu_selected_button)

			printGui(pattern_number, midi_and_channel, selected_note_and_octave, selected_beat, pattern[:], selected_menu_button = None)
			
if __name__ == "__main__":
	data_storage = DataStorage()
	keypad = Keypad()
	main(keypad, data_storage, 1, "M1c1", 1)
