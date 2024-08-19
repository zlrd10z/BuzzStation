from gui_tracker import createScreenMatrix, fillMatrix, drawNumbersAndFrames, markTrackWithSampleName, printScreenMatrix, drawSwingBPMnMasterVolumeValue
from changeTextColor import changeStringBgColor, changeStringFontColor

formatTextAsSelected = lambda text: changeStringBgColor("grey", changeStringFontColor("black", text))

def createVerticalGreyLines(screen_matrix):
	# screen's hight of 17 characters:
	for y in range(17):
		track_position = 2
		# 8 tracks:
		for i in range(8):
			# 5 characters ength for track:
			for j in range(5):
				# each second i
				if y % 2 == 1:
					screen_matrix[y][track_position + j] = changeStringBgColor("black grey", screen_matrix[y][track_position + j])
			track_position += 6
	
	return screen_matrix

def drawInformationThatItIsPlalist(screen_matrix):
	# x is char on x axis, where the tracks ends, and the song info starts:
	x = 2 + 6*8
	info_text = " [Playlist]" 
	# Draw "Song Name:" text
	for i in range(64 - x):
		if i <= len(info_text)-1:
			screen_matrix[0][x + i] = changeStringBgColor("blue", info_text[i])
	return screen_matrix

def drawMenu(screen_matrix, selected = None):
	gui_width = 64
	# x is char on x axis, where the tracks ends, and the song info starts:
	x = 2 + 6*8
	info_text = "    Menu: "
	# Draw "Song Name:" text
	for i in range(gui_width - x):
		if i <= len(info_text)-1:
			screen_matrix[5][x + i] = changeStringBgColor("blue", info_text[i])

	# playlist button:
	button_text = " Save "
	for i in range(gui_width - x):
		if i <= len(button_text) - 1:
			if selected == 0:
				screen_matrix[6][x + i] = formatTextAsSelected(button_text[i])
			else:
				screen_matrix[6][x + i] = button_text[i]

	# clone pattern:
	button_text = " Load "
	for i in range(gui_width - x):
		if i <= len(button_text)-1:
			if selected == 1:
				screen_matrix[6][x + i + 7] = formatTextAsSelected(button_text[i])
			else: 
				screen_matrix[6][x + i + 7] = button_text[i]

	return screen_matrix

def drawInfoAboutInstrument(screen_matrix, selected_instrument):
	gui_width = 64
	x = 2 + 6*8
	text_line_1 = "Inst. info:"
	for i in range(len(text_line_1)):
		screen_matrix[8][x + i + 1] = changeStringBgColor("blue", text_line_1[i])
	
	lines = []
	if selected_instrument == "Drums":
		text_line_1 = " Drums and"
		text_line_2 = "  Samples"
		lines = [text_line_1, text_line_2]
	elif selected_instrument == "Empty":
		text_line_1 = "  [insert]"
		text_line_2 = "to add midi"
		lines = [text_line_1, text_line_2]
		
	else:
		text_line_1 = "Midi Port: " + selected_instrument[1]
		text_line_2 = " Channel: " + selected_instrument[-1]
		if len(selected_instrument) == 5:
			text_line_2 = " Channel " + selected_instrument[-2:]
		lines = [text_line_1, text_line_2]
		

	for i in range(len(lines)):
		for j in range(len(lines[i])):
			screen_matrix[9 + i][x + j + 1] = changeStringBgColor("blue", lines[i][j])

	
	return screen_matrix

def drawPatterns(screen_matrix, selected_pattern, playlist, first_number, pattern_cursor):
	if pattern_cursor is not None:
		pattern_cursor[1] = pattern_cursor[1] - 1
	
	x = 2
	for i in range(len(playlist)):
		for j in range(len(playlist[i])):
			if j < first_number + 16:
				if playlist[i][j] is not None:
					pattern_number_length = len(str(playlist[i][j]))
					for k in range(pattern_number_length):
						if pattern_cursor is not None and pattern_cursor[0] == i and pattern_cursor[1] == j:
							screen_matrix[j+1][x+k] = formatTextAsSelected(str(playlist[i][j])[k])
						elif j % 2 == 0:
							screen_matrix[j+1][x+k] = changeStringBgColor("black grey", str(playlist[i][j])[k])
						else:
							screen_matrix[j+1][x+k] = str(playlist[i][j])[k]
		x += 6
	return screen_matrix

def main(list_of_instruments, bpm_value, swing_value, vol_value, playlist, menu_selected = None, gui_cursor = None, first_number = 1):
	if gui_cursor is not None:
		if gui_cursor[1] == 0:
			selected_pattern = gui_cursor[0]
			pattern_cursor = None
		else:
			pattern_cursor = gui_cursor
			selected_pattern = None
	else:
		selected_pattern = None
		pattern_cursor = None
	
	screen_matrix = createScreenMatrix()
	screen_matrix = fillMatrix(screen_matrix)
	screen_matrix = drawNumbersAndFrames(first_number, screen_matrix = screen_matrix)
	screen_matrix = markTrackWithSampleName(screen_matrix = screen_matrix, list_of_samples = list_of_instruments, selected = selected_pattern)
	screen_matrix = drawInformationThatItIsPlalist(screen_matrix)
	screen_matrix = drawMenu(screen_matrix, selected = menu_selected)
	screen_matrix = drawSwingBPMnMasterVolumeValue(screen_matrix, bpm_value, swing_value, vol_value)
	if selected_pattern is not None:
		screen_matrix = drawInfoAboutInstrument(screen_matrix, list_of_instruments[selected_pattern])
	screen_matrix = createVerticalGreyLines(screen_matrix)
	screen_matrix = drawPatterns(screen_matrix, selected_pattern, playlist, first_number, pattern_cursor)
	printScreenMatrix(screen_matrix)
	
if __name__ == "__main__":
	playlist = [[1, None, 2, None],[4000,400,32,134]]
	selected_pattern = [1, 2]
	main(list_of_instruments = ["Drums", "M1C1"], bpm_value = 200, swing_value = 50, vol_value = 90, playlist = playlist, gui_cursor = [0, 3])
	#cursor [instrument, quareternote]
