from gui import gui_warning_window
from libs.keypad import Keypad
from core.data_storage import DataStorage

def createEmptyPattern():
	pattern = []
	for i in range(16):
		l = []
		pattern.append(l)
	#                  [note, note length, volume]
	#    pattern[0].append(["C#5", 1, 8])

	return pattern


def pianoroll(keypad, data_storage, pattern_number):
	
	notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	selected_note_and_octave = "C5"
	selected_beat = 0
	
	
	# Check is this pattern exist or this is new pattern:
	pianoroll_patterns_order = data_storage.get_data("pianoroll_patterns_order")
	if pattern_number in pianoroll_patterns_order:
		pattern = data_storage.pianorollPatternOperations("get pattern", pattern_number)
		
	else:
		#create new pattern:
		pianoroll_patterns_order.append(pattern_number)
		pattern = createEmptyPattern()
		data_storage.pianorollPatternOperations("put pattern", pattern)
		data_storage.put_data("pianoroll_patterns_order", pianoroll_patterns_order)
	
	while True:
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
			print(selected_note_and_octave, selected_beat)	
			
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

					
				print(pattern[selected_beat])
				
if __name__ == "__main__":
	data_storage = DataStorage()
	keypad = Keypad()
	pianoroll(keypad, data_storage, 1)
