from changeTextColor import changeStringFontColor, changeStringBgColor

# Lambdas:
clear = lambda: os.system("clear")

# 64x18 characters:
gui_height = 17 #terminal command line is taking one line
gui_width = 64

# Create matrix 16 x 64 chars
def createScreenMatrix():
	screen_matrix = []
		
	for i in range(gui_height):
		row_matrix = []
		for j in range(gui_width):
			row_matrix.append("")
		screen_matrix.append(row_matrix)
		
	return screen_matrix

screen_matrix = createScreenMatrix()

def drawFrame():
	for i in range(len(screen_matrix)):
		for j in range(len(screen_matrix[i])):
			if i < 1 or i > len(screen_matrix) - 4:
				screen_matrix[i][j] = changeStringBgColor("blue", " ")
				
			elif j < 2 or j > len(screen_matrix[i]) - 8:
				screen_matrix[i][j] = changeStringBgColor("blue", " ")
				screen_matrix[i][j] = changeStringBgColor("blue", " ")

			else:
				screen_matrix[i][j] = " "
			
drawFrame()
octave = 5
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]

def drawPiano(y_position, x_poistion):
	for i in range(13):
		note = " "
		if len(notes[i]) == 2:
			note = notes[i] + str(octave)
		else:
			note += notes[i] + str(octave)

		if i > 11:
			note = note[:-1] + str(octave + 1)
			
		print(note)
		for j in range(4):
			if i == 1 or i == 3 or i == 6 or i == 8 or i == 10:
				pass
			else:
				screen_matrix[y_position - i][j+x_poistion] = changeStringBgColor("grey", " ")
				
			if j == 0:
				pass
			else:
				#print(note)
				note_part = changeStringFontColor("black", note[j-1])
				note_part = changeStringBgColor("grey", note_part)
				screen_matrix[y_position - i][j+x_poistion+3] = note_part
				
drawPiano(13,2)

def drawQuarterTime():
	x_position = 9
	x = 0
	for i in range(16):
		char_number = chr(0x2488 + i)
		if i % 4 == 0:
			screen_matrix[0][x_position + x] = changeStringFontColor("black", changeStringBgColor("blue", char_number))
		else:
			screen_matrix[0][x_position + x] = changeStringBgColor("blue", char_number)
		x += 3
drawQuarterTime()		

def drawPatternNumber(pattern_number = 1):
	text_to_print = "Pattern: " + str(pattern_number)
	axisx_start_printing = (gui_width - len(text_to_print))
	for i in range(len(text_to_print)):
		screen_matrix[gui_height-1][axisx_start_printing + i] = changeStringBgColor("blue", text_to_print[i])

drawPatternNumber()

def drawSwingBPMValueAndMidiChannelNumber(bpm_value = 100, swing_value = 40, channel_number = 1):
	
	text_to_print = "BPM: " + str(bpm_value) + 8 * " " + "Swing: " + str(swing_value) + 8 * " " + "Channel: " + str(channel_number)
	for i in range(len(text_to_print)):
		screen_matrix[gui_height-1][i+2] = changeStringBgColor("blue", text_to_print[i])


drawSwingBPMValueAndMidiChannelNumber()

def drawIsPlaying(is_playing = False):
	playing_info = "Pause"
	if is_playing: playing_info = "Playing"
	axisx_start_printing = int(gui_width / 2 - len(playing_info))
	for i in range(len(playing_info)):
		screen_matrix[gui_height-3][axisx_start_printing + 1 + i] = changeStringBgColor("blue", playing_info[i])

drawIsPlaying(True)

def drawButtons(selected = None):
	button_playlist = " Playlist "
	button_new = " New "
	button_clone = " Clone "
	button_previous_pattern = " ⇽ "
	button_next_pattern = " ⇾ "
	
	toDraw =  button_previous_pattern + "?" + button_playlist + "?" + button_new + "?" +  button_clone + "?" + button_next_pattern
	question_mark_counter = 0
	for i in range(len(toDraw)):
		if toDraw[i] == "?": 
			question_mark_counter += 1
			
		elif question_mark_counter == selected:
			screen_matrix[gui_height-2][15 + i] = changeStringBgColor("grey", changeStringFontColor("black",toDraw[i] ) )
		else:
			screen_matrix[gui_height-2][15 + i] = toDraw[i]
		
		
drawButtons()		
		
def printGUI():
	toprint = ""
	for i in range(len(screen_matrix)):
		for j in range(len(screen_matrix[i])):
			toprint += screen_matrix[i][j]
	print(toprint)

printGUI()
