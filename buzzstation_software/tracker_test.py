from gui import gui_tracker
from libs.keypad import Keypad
from core.data_storage import DataStorage
from core.pick_file import getFilename



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

def changeNote(operation, note_and_octave):
	notes_string_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	
	if operation == "semitone down":
		octave = note_and_octave[-1:]
		note = note_and_octave[:-1]
		note_index = notes_string_list.index(note)
		# if sound is eg C5 then switch to note B4, octave cannot be lower than 1:
		if note_index == 0 and octave >= 2: 
			note = notes_string_list[len(notes_string_list) - 1:]
			octave = str( int(octave) - 1 )
		# If note is eg C#5, then switch note to C5	
		else: 
			note_index -= 1
			note = notes_string_list[note_index]
		new_note = note + octave
			
	if operation == "semitone up":	
			# Change note value up:
		if tracker_cursor[2] == 0:
			octave = note_and_octave[-1:]
			note = note_and_octave[:-1]
			note_index = notes_string_list.index(note)
			# if sound is eg B5 then switch to note C6, octave cannot be higher than 7:
			if note_index == len(notes_string_list) - 1 and octave <= 7: 
				note = notes_string_list[0]
				octave = str( int(octave) + 1 )

			# If note is eg C#5, then switch note to C5	
			else: 
				note_index += 1
				note = notes_string_list[note_index]
			new_note = note + octave
		
	return new_note

def main(keys, data_storage, pattern_number):

	volume_string_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
	tracker_cursor = [0, 0, 0]
	
	potentiometers_previous_values = [None, None, None]
	
	# Create new empty pattern:
	data_storage.put_data("drums_patterns", createNewEmptyPattern())
	data_storage.put_data("drums_patterns_order", pattern_number)
	samples = data_storage.get_data("samples")
	pattern = data_storage.drumsPatternOperations("get pattern", pattern_number)
	
	while True:
		bpm = data_storage.get_data("bpm")
		swing = data_storage.get_data("swing")
		bvol = data_storage.get_data("bvol")
		
		if bpm != potentiometers_previous_values[0] or swing == potentiometers_previous_values[1] or bvol != potentiometers_previous_values[2]:
			potentiometers_previous_values[0] = bpm
			potentiometers_previous_values[1] = swing
			potentiometers_previous_values[2] = bvol
			#update gui here...
		
		
		if tracker_cursor[0] == 0 and tracker_cursor[2] != 0: tracker_cursor[2] = 0
		
		key = keys.check_keys()
		if key != '':
						
			# [Escape] key - back to playlist:
			if key == '1':
				break
			
			# Direction key - down:
			if key == '8':
				if tracker_cursor[1] + 1 < 17:
					tracker_cursor[1] += 1
				else: tracker_cursor[1] == -1
			
			# Direction key - up:
			if key == '2':
				if tracker_cursor[1] - 1 > -1:
					tracker_cursor[1] -= 1
					if tracker_cursor == 0:
						tracker_cursor[2] = 0
				else: tracker_cursor[1] == 16
			
			# Direction key = right:
			if key == '6':
				# If actual selected sample is not empty, user can move to pick next empty sample:
				if tracker_cursor[1] == 0 and samples[tracker_cursor[0]] != "Empty":
					tracker_cursor[0] += 1
				
				# If cursor is on playlist and next track from the right is choosen, let user to move cursor to next sample playlist:
				if tracker_cursor[2] == 0:
					tracker_cursor[2] += 1
				elif tracker_cursor[2] == 1:
					if tracker_cursor[1] != 0 and samples[tracker_cursor[0] + 1] != "Empty":
						tracker_cursor[0] += 1
			# Direction key = right:
			if key == '4':
				# Cursor on samples level:
				if tracker_cursor[1] == 0 and tracker_cursor[0] - 1 >= 0:
					tracker_cursor[0] -= 1
				
				# Cursor on Playlist level:
				elif tracker_cursor[1] != 0:
					if tracker_cursor[2] == 1:
						tracker_cursor[2] -= 1
					elif tracker_cursor[2] == 0:
							tracker_cursor[2] = 1
							tracker_cursor[0] -= 1	
	
			if key == '7':
				# Add note with volume:
				if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
					pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ["C5", 'F']
				
				else:
					# Change note value down:
					if tracker_cursor[2] == 0:
						note_and_octave = pattern[tracker_cursor[0]][tracker_cursor[1]-1][tracker_cursor[2]]
						new_note = changeNote("semitone down", note_and_octave)
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
				pattern = data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)
				
				if key == '9':
					# Add note with volume:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ["C5", 'F']

					else:
						
						# semitone up:
						if tracker_cursor[2] == 0:
							note_and_octave = pattern[0][1][2]
							new_note = changeNote("semitone up", note_and_octave)
							pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = new_note


						# Change note's volume value:
						if tracker_cursor[2] == 1:
							volume = pattern[0][1][2]
							volume_index = volume_string_list.index(volume)
							if volume_index < len(volume_string_list) - 1:
								volume_index += 1
								volume = volume_string_list[volume_index]
							pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = volume
							
					data_storage.put_data("drums_last_added_note", [pattern[tracker_cursor[0]][tracker_cursor[1] - 1][0], 
								pattern[tracker_cursor[0]][tracker_cursor[1] - 1][1]])

					# update pattern in data storage:
					pattern = data_storage.drumsPatternOperations("update pattern", pattern_number, new_pattern = pattern)	
	
			# Insert key:
			if key == '5':
				# If cursor is on samples level, insert sample / change sample to other one:
				if tracker_cursor[1] == 0:
					# Choose sample from disk with getFilename function and get path to choosen sample:
					samples[tracker_cursor[0]] = getFilename("sample")
					data_storage.put_data("samples", samples)
					
				# if cursor is on playlist:
				elif tracker_cursor[1] > 0:
					# if note is empty, add last added note:
					if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = data_storage.get_data("drums_last_added_note")
					# if field for note is not empty, delete note:
					else:
						pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = []
					
					
			# Escape key:
			if key == '1':
				patternIsEmpty = checkIfPatternIsEmpty()
				if patternIsEmpty:
						# Delete pattern from patterns list and pattern orders list:
						data_storage.drumsPatternOperations("delete_pattern", pattern_number)
				# exit to playlist:
				break


					
if __name__ == "__main__":
	keys = Keypad()
	data_storage = DataStorage()
	main(keys, data_storage)
