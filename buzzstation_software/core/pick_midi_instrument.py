from gui.txtcolor import text_font_color, text_bg_color
from gui.gui_tracker import create_screen_matrix, fill_matrix, print_screen_matrix
from libs.keypad import Keypad
import os

# Format text as selected:
selected_text = lambda text: text_bg_color("grey", text_font_color("black", text))

clear_screen = lambda: os.system("clear")

def create_instruments_dic():
	midi_instruments = {}
	with open("midi_instruments_list.txt", "r") as file:
		for line in file:
			line = line.split("	")
			if line[1] not in midi_instruments:
				midi_instruments[line[1]] = {}
			midi_instruments[line[1]][line[2].replace("\n", "")] =  line[0]
	return midi_instruments

def draw_window(screen_matrix, midi_instruments, instrument_type, midi_output, selected):
	# Draw box with space on top for text:
	for y in range(len(screen_matrix)):
		for x in range(len(screen_matrix[y])):
			if x == 0 or x == len(screen_matrix[y]) - 1:
				screen_matrix[y][x] = text_bg_color("blue", "┃")
				if y == 0:
					screen_matrix[y][x] = text_bg_color("blue", " ")
				if x == 0 and y == 1:
					screen_matrix[y][x] = text_bg_color("blue", "┏")
				if x == len(screen_matrix[y]) - 1 and y == 1:
					screen_matrix[y][x] = text_bg_color("blue", "┓")
				if x == 0 and y == len(screen_matrix) - 1:
					screen_matrix[y][x] = text_bg_color("blue", "┗")
				if x == len(screen_matrix[y]) - 1 and y == len(screen_matrix) - 1:
					screen_matrix[y][x] = text_bg_color("blue", "┛")
			elif y == 1 or y == len(screen_matrix) - 1:
				screen_matrix[y][x] = text_bg_color("blue", "━")
				
			else:
				screen_matrix[y][x] = text_bg_color("blue", " ")

	# Put title text on the screen:
	channel = midi_output[4:]
	text = "Select instrument for MIDI " + midi_output[1] + " Channel " + channel + ":"
	
	#Center text on screen:
	text_start = (len(screen_matrix[0]) - len(text)) / 2
	text_start = int(text_start) 
	
	for i in range(len(text)):
		screen_matrix[0][text_start + i] = text_bg_color("blue", text[i])
	
	
	to_print = None
	if instrument_type == None:
		to_print = list(midi_instruments.keys())
		if selected > 12:
			to_print = ["…"] + to_print[13:]
			selected -= 12
		else:
			to_print = to_print[:14]
			to_print[-1] = "…" 
	else:
		to_print = list(midi_instruments[instrument_type].keys())


	y = 2
	x = 1
	for i in range(len(to_print)):
		for j in range(len(to_print[i])):
			if i == selected:
				screen_matrix[y + i][x + j] = selected_text(to_print[i][j])
			else:
				screen_matrix[y + i][x + j] = text_bg_color("blue", to_print[i][j])


				
def gui(midi_instruments, midi_output, selected, instrument_type = None):
	screen_matrix = create_screen_matrix()
	screen_matrix = fill_matrix(screen_matrix)
	draw_window(screen_matrix, midi_instruments, instrument_type, midi_output, selected)
	clear_screen()
	print_screen_matrix(screen_matrix)

def menu_select_instrument(keys, midi_instruments, instrument_type, midi_output):
	instruments = list(midi_instruments[instrument_type].keys())
	selected = 0
	gui(midi_instruments, midi_output, selected, instrument_type)
	
	
	while True:
		key = keys.check_keys()
		if key != "":
			# Down key:
			if key == "2" and selected > 0:
				selected -= 1

			# Up key:
			if key == "8" and selected < len(instruments) - 1:
				selected += 1

			# Accept key:
			if key == "5":
				result = (instruments[selected], int(midi_instruments[instrument_type][instruments[selected]]))
				return result

			# Esc Key:
			if key == "1":
				break

			gui(midi_instruments, midi_output, selected, instrument_type)

def menu_instrument_types(keys, midi_instruments, midi_output):
	instrument_types = list(midi_instruments.keys())
	selected = 0
	result = None
	gui(midi_instruments, midi_output, selected)
	
	
	while True:
		key = keys.check_keys()
		if key != "":
			# Down key:
			if key == "2" and selected > 0:
				selected -= 1

			# Up key:
			if key == "8" and selected < len(instrument_types) - 1:
				selected += 1

			# Accept key:
			if key == "5":
				result = menu_select_instrument(keys, midi_instruments, instrument_types[selected], midi_output)
				
				if result is not None:
					return result

			# Esc Key:
			if key == "1":
				break
				
			gui(midi_instruments, midi_output, selected)
	
def main(keys, midi_output):
	midi_instruments = create_instruments_dic()
	result = menu_instrument_types(keys, midi_instruments, midi_output)
	return result
	
	
	

if __name__ == "__main__":
	keys = Keypad()
	result = main(keys, midi_output = "M1CH1")
	print(result)
