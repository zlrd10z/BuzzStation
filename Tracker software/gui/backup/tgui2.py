import os, sys
import time
from changeTextColor import changeStringBgColor, changeStringFontColor

# Lambdas:
clear = lambda: os.system("clear")

# 64x18 characters:
gui_height = 17 #terminal command line is taking one line
gui_width = 64

class TrackerGUI:
	# Create matrix 16 x 64 chars
	def createScreenMatrix(self):
		screen_matrix = []
		for i in range(gui_height):
			screen_matrix.append([])
		return screen_matrix

	# Append matrix with spaces characters:
	def fillMatrix(self, screen_matrix):
		for i in range(gui_height):
			for j in range(gui_width):
				screen_matrix[i].append(" ")	
		return screen_matrix

	# This function: 
	# Draws numbers on the left, from 1-16, which represents quaternotes in pattern
	# Draws 1char-width frames which separates 8 tracks
	# Fills with solid color part of right part of the screen, which create space for other information like actual BPM value
	def drawNumbersAndFrames(self, first_number, screen_matrix):
		for i in range(16):
			id_number = str(first_number + i)
			#print(id_number)
			i += 1

			# Draw Numbers 1-16
			if(len(id_number) > 1):	
				screen_matrix[i][0] = changeStringBgColor("blue", id_number[0])
				screen_matrix[i][1] = changeStringBgColor("blue", id_number[1])
				# Mark each bar with yellow:
				if int(id_number) % 4 == 1:
					screen_matrix[i][0] = changeStringFontColor("black", screen_matrix[i][0])
					screen_matrix[i][1] =  changeStringFontColor("black", screen_matrix[i][1])

			else:
				screen_matrix[i][1] = changeStringBgColor("blue", id_number)
				screen_matrix[i][0] = changeStringBgColor("blue", " ")
				if int(id_number) % 4 == 1: 
					screen_matrix[i][1] = changeStringFontColor("black", screen_matrix[i][1])

			# Draw horizontal frame at the top on the screen:
			# On that line, there will be displayed names of samples, assigned to each track
			for j in range(len(screen_matrix[0])):
				screen_matrix[0][j] = changeStringBgColor("blue", " ")

			# Draw vertical frames and fill on the right side:
			for j in range(len(screen_matrix)):
				tracks = 1
				for k in range(len(screen_matrix[0])):
					if(k % 6 == 1 and k > 1 and tracks <= 8):
						screen_matrix[j][k] = changeStringBgColor("blue", " ")
						tracks += 1
					elif(tracks > 8):
						screen_matrix[j][k] = changeStringBgColor("blue", " ")
		return screen_matrix

	def markTrackWithSampleName(self, list_of_samples, screen_matrix):
			# Samples are stored as path to file
			# Extracting names and abbreviate to first 4 letters with ellipsis on the end:
			for i in range(len(list_of_samples)):
				sample_path = list_of_samples[i]
				sample_path = sample_path.split("/")
				sample_name = sample_path[-1]
				sample_name = sample_name.split(".")
				sample_name = sample_name[0]
				sample_name = sample_name[:4] + "…"
				list_of_samples[i] = sample_name

			if(len(list_of_samples) < 8):
				x = 8 - len(list_of_samples)
				for i in range(x):
					list_of_samples.append("Empty")

			tracks = 1
			for i in range(len(screen_matrix[0])):
				if(i % 6 == 2 and tracks <= 8):
					for j in range(5):
						screen_matrix[0][i+j] = changeStringBgColor("blue", list_of_samples[tracks-1][j])
					tracks += 1
			return screen_matrix
	
	def drawFieldsForNotes(self, screen_matrix):
		# Three is 8 tracks with length of 16, each note has 5 chars for note value and it's volume, between that note info there is 1 char of free space
		for i in range(16):
			x = 2
			for j in range(8):
				for k in range(5):
					if k != 3: screen_matrix[i+1][x+k] = "."
				x += 6
		return screen_matrix
	
	def drawSongName(self, screen_matrix, song_name = None):
		# x is char on x axis, where the tracks ends, and the song info starts:
		x = 2 + 6*8
		info_text = " Song name:"
		# Draw "Song Name:" text
		for i in range(gui_width - x):
			if i <= len(info_text)-1:
				screen_matrix[0][x + i] = changeStringBgColor("blue", info_text[i])
			
		if song_name is not None:
			# Center filename:
			if len(song_name) < gui_width - x:
				how_many_fill = gui_width - x - len(song_name)
				how_many_fill = (how_many_fill / 2) - 1
				song_name = " " * int(how_many_fill) + song_name
			
			# Draw filename (max two lines):
			for j in range(2):
				for i in range(gui_width - x):
					if len(song_name) == 0: break
					
					#if name len exceed space for song name:
					if j == 1 and i == gui_width - x - 1 and len(song_name) > 1:
						screen_matrix[1+j][x + i] = changeStringBgColor("blue", "…")
					else:
						screen_matrix[1+j][x + i] = changeStringBgColor("blue", song_name[:1])
						song_name = song_name[1:]
		return screen_matrix
	
	def drawPatternNumber(self, screen_matrix, pattern_numer = 1):
		# x is char on x axis, where the tracks ends, and the song info starts:
		x = 2 + 6*8
		info_text = " Pattern: " + str(pattern_numer)
		# Draw "Song Name:" text
		for i in range(gui_width - x):
			if i <= len(info_text)-1:
				screen_matrix[0][x + i] = changeStringBgColor("blue", info_text[i])
		return screen_matrix
	
	def drawSwingBPMnMasterVolumeValue(self, screen_matrix, bpm_value = 140, swing_value = 0, vol_value = 10):
		# x is char on x axis, where the tracks ends, and the song info starts:
		x = 3 + 6*8
		info_text = "BPM:    Swing:  mVOL:   "
		for i in range(3):
			value_to_print = 0
			if i == 0: value_to_print = bpm_value
			if i == 1: value_to_print = swing_value
			if i == 2: value_to_print = vol_value
			value_to_print = str(value_to_print)
			how_many_fills = 3 - len(value_to_print)
			value_to_print = "0" * how_many_fills + value_to_print
			for j in range(11):
				if j < 8:
					screen_matrix[1+i][x+j] = info_text[:1]
					info_text = info_text[1:]
				else:
					screen_matrix[1+i][x+j] = value_to_print[:1]
					value_to_print = value_to_print[1:]
		return screen_matrix
	
	def drawMenu(self, screen_matrix):
		# x is char on x axis, where the tracks ends, and the song info starts:
		x = 2 + 6*8
		info_text = "    Menu: "
		# Draw "Song Name:" text
		for i in range(gui_width - x):
			if i <= len(info_text)-1:
				screen_matrix[5][x + i] = changeStringBgColor("blue", info_text[i])
		# playlist button:
		button_text = " Playlist  "
		for i in range(gui_width - x):
			if i <= len(button_text)-1:
				screen_matrix[6][x + i + 1] = button_text[i]
		
	
		button_text = " New "
		for i in range(gui_width - x):
			if i <= len(button_text)-1:
				screen_matrix[7][x + i + 4] = button_text[i]
		

		button_text = " Clone "
		for i in range(gui_width - x):
			if i <= len(button_text)-1:
				screen_matrix[8][x + i + 3] = button_text[i]
		return screen_matrix
	
	def drawIsPlaying(self, screen_matrix, is_playing = False):
		# x is char on x axis, where the tracks ends, and the song info starts:
		x = 2 + 6*8
		info_text = "Pause"
		if is_playing: info_text = "Playing"
		how_many_fills = ((gui_width - x) - len(info_text)) / 2
		info_text = " " * int(how_many_fills) + info_text
		
		# Draw "Song Name:" text
		for i in range(gui_width - x):
			if i <= len(info_text)-1:
				screen_matrix[16][x + i] = changeStringBgColor("blue", info_text[i])
		return screen_matrix

	# create string from chars matrix (screen_matrix) and print it out
	def printScreenMatrix(self, screen_matrix):
		frame = ""
		for i in range(len(screen_matrix)):
			for j in range(len(screen_matrix[0])):
				frame += screen_matrix[i][j]
		print(frame)
	


	def createAndPrint(self, list_of_samples):
		#clear()
		screen_matrix = self.createScreenMatrix()
		sceeen_matrix = self.fillMatrix(screen_matrix)
		screen_matrix = self.drawNumbersAndFrames(1, screen_matrix)
		screen_matrix = self.markTrackWithSampleName(list_of_samples, screen_matrix)
		screen_matrix = self.drawPatternNumber(screen_matrix)
		screen_matrix = self.drawFieldsForNotes(screen_matrix)
		screen_matrix = self.drawSwingBPMnMasterVolumeValue(screen_matrix)
		screen_matrix = self.drawMenu(screen_matrix)
		screen_matrix = self.drawIsPlaying(screen_matrix)
		self.printScreenMatrix(screen_matrix)



t_GUI = TrackerGUI()
t_GUI.createAndPrint(["folder/kick_deep_132.mp3"])

try:
	while True: pass
except Exception as e:
	print(e)
finally:
	pass
