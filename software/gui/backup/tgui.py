
import os, sys
import time

clear = lambda: os.system("clear")

#64x18 characters
gui_height = 17 #terminal command line is taking one line
gui_width = 64

# Colours:
DARK_PURPLE = "\033[38;5;93m"
BG_BLUE = "\033[48;5;93m"
RESET = "\033[0m"
BG_GREEN = "\033[48;5;10m"

print(f"{DARK_PURPLE}test{RESET}" * 5)
#clear()
fill_char = chr(0x2588)

#print(fill_char * 64)

# Create Matrix which would be printed as GUI
screen_matrix = []
for i in range(gui_height):
	screen_matrix.append([])

def changeCharBg(color, char):
	colored_char = ""
	if color == "green":
		colored_char = (f"{BG_GREEN}{char}{RESET}")
	elif color == "blue":
		colored_char = (f"{BG_BLUE}{char}{RESET}")
	else: pass
	return colored_char

def drawBackground():
	#fill = changeCharBg("green", " ")
	fill = " "
	for i in range(gui_height):
		for j in range(64):
			screen_matrix[i].append(fill)

def drawNumbersAndFrames(first_number):
	def reverseColor(char):
		return (f"{BG_BLUE}{char}{RESET}")

	for i in range(16):
		id_number = str(first_number + i)
		print(id_number)


		i += 1
		# Draw Numbers 1-16
		if(len(id_number) > 1):
			screen_matrix[i][0] = reverseColor(id_number[0]) 
			screen_matrix[i][1] = reverseColor(id_number[1])

		else:
			screen_matrix[i][1] = reverseColor(id_number)
			screen_matrix[i][0] = reverseColor(" ")

		# Draw horizontal frame:
		for j in range(len(screen_matrix[0])):
			screen_matrix[0][j] = reverseColor(" ")

		# Draw vertical frames and fill on the right side:
		for j in range(len(screen_matrix)):
			tracks = 1
			for k in range(len(screen_matrix[0])):
				if(k % 6 == 1 and k > 1 and tracks <= 8):
					screen_matrix[j][k] = reverseColor(" ")
					tracks += 1
				elif(tracks > 8):
					screen_matrix[j][k] = reverseColor(" ")
drawBackground()
drawNumbersAndFrames(1)
#print(screen_matrix)

def printScreenMatrix():
	frame = ""
	for i in range(len(screen_matrix)):
		for j in range(len(screen_matrix[0])):
			frame += screen_matrix[i][j]
	print(frame)

clear()
printScreenMatrix()
#print(screen_matrix[0][0])

try:
	while True: pass
except Exception as e:
	print(e)
finally:
	pass
