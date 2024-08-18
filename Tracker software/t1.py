import asyncio
from libs import keypad
from gui import gui_playlist
from core import potentiometers
from core import potentiometer_values_transform
import time
import os
import copy

keys = keypad.Keypad()
# Values from potentiometers:
bpm = 0
swing = 0
bvol = 0
timeBetweenQuarterNotes = 0

# Song variables
playlist_list_of_instruments = ["Drums"]
song_playlist = []

# Lambdas:
clear_screen = lambda: os.system("clear")
GUIplaylist = lambda gui_cursor, playlist, menu_selected, list_of_instruments: gui_playlist.main(
										list_of_instruments = list_of_instruments,
										bpm_value = bpm,
										swing_value = swing,
										vol_value = bvol,
										playlist = playlist,
										gui_cursor = gui_cursor,
										menu_selected = menu_selected,
										)

def potentiometersOperations():
	global bpm, swing, bvol, timeBetweenQuarterNotes
	pots_values = potentiometers.returnPotentiometersValues()
	
	bpm_newvalue = int(potentiometer_values_transform.bpmFromPotentiometer0(pots_values[0]))
	if bpm_newvalue - bpm > 1 or bpm - bpm_newvalue > 1:
		bpm = bpm_newvalue
	
	swing_newvalue = int(potentiometer_values_transform.swingFromPotentiometer1(pots_values[1]))
	if swing_newvalue - swing > 1 or swing - swing_newvalue > 1:
		swing = swing_newvalue
		
	bvol_newvalue = int(potentiometer_values_transform.volumeFromPotentiometer2(pots_values[2]))
	if bvol_newvalue - bvol > 1 or bvol - bvol_newvalue > 1:
		bvol = bvol_newvalue
		
	timeBetweenQuarterNotes = potentiometer_values_transform.countTimePerQuarterNote(bpm)


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

def appendInstrumentListWithEmpty(how_many_empty):
	global playlist_list_of_instruments
	for i in range(how_many_empty):
		playlist_list_of_instruments.append("Empty")

		
def playlist_loop():
	global song_playlist
	def createEmptySongPlaylist():
		instrument = []
		for i in range(16):
			instrument.append(" ")
		song_playlist.append(instrument)
	
	createEmptySongPlaylist()
		
	playlist_cursor = [0, 0]
	# Playlist loop:
	previous_printed_values = [None, None, None]
	
	while True:
		potentiometersOperations()

				
		cursor = playlist_cursor[:]
	
		#Update screen, if any potetniometer values changed:
		if previous_printed_values[0] == bpm and previous_printed_values[1] == swing and previous_printed_values[2] == bvol:
			#print(previous_printed_values[0], cursor)
			pass
		else:
			clear_screen()
			GUIplaylist(gui_cursor = cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
			previous_printed_values[0] = bpm
			previous_printed_values[1] = swing
			previous_printed_values[2] = bvol
		
			
		key = keys.check_keys()
		if key != "":
			if key == '2':
				if playlist_cursor[1] > 0:
					playlist_cursor[1] -=  1
					clear_screen()
					GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
							
				
			if key == '8':
				playlist_cursor[1] += 1
				if playlist_cursor[1] > len(song_playlist[0]):
					for i in range(len(song_playlist)):
						for j in range(16):
							song_playlist[i].append(" ")
					
				clear_screen()
				GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
				
					
			if key == '4':
				if playlist_cursor[0] > 0: 
					playlist_cursor[0] -= 1
					clear_screen()
					GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
			
			if key == '6':
				if playlist_cursor[0] + 1 == len(playlist_list_of_instruments):
					for i in range(8): playlist_list_of_instruments.append("Empty")

					
				if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
					playlist_cursor[0] += 1
					clear_screen()
					GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
					
					
			if key == '7':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) - 1 == 0:
							channel = 16
						else:
							channel = int(midi_instrument[3:]) - 1
						midi_instrument = midi_instrument[:3] + str(channel)
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
						clear_screen()
						GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
				
			if key == '9':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if playlist_list_of_instruments[playlist_cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) + 1 == 17:
							channel = 1
						else:
							channel = int(midi_instrument[3:]) + 1
						midi_instrument = midi_instrument[:3] + str(channel)
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
						clear_screen()
						GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None)
			
			if key == '3':
				selected = 0
				clear_screen()
				GUIplaylist(cursor = None, playlist = song_playlist, menu_selected = selected, first_note = 1)
				
				while True:
					key = keys.check_keys()
					if key != "":
						if key == '4' or key == '6':
							new_selected = selected
							if key == '4':
								if selected == 1:
									new_selected = 0

							if key == '6':
								if selected == 0:
									new_selected = 1
							
							if new_selected != selected:
								clear_screen()
								GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = new_selected, list_of_instruments = playlist_list_of_instruments[:])
								selected = new_selected
	
						
						if key == '5':
							if selected == 0:
								saveSong()
							else:
								loadSong()
								
							clear_screen()
							GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
							break
							
						if key == '1':
							clear_screen()
							GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
							break

			
			if key == '*':
				playSong()
				
			if key == '5':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					# Assign new midi output port to an empty slot:
					if playlist_list_of_instruments[cursor[0]] == "Empty":
						playlist_list_of_instruments[cursor[0]] = "M1c1"
						createEmptySongPlaylist()

					# Change midi output port
					elif playlist_list_of_instruments[cursor[0]] != "Empty":
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						midi_channel = midi_instrument[2:]
						midi_output = int(midi_instrument[1])

						if midi_output == 3:
							midi_output = 1
						else:
							midi_output += 1
						playlist_list_of_instruments[playlist_cursor[0]] = "M" + str(midi_output) + midi_channel
					clear_screen()
					GUIplaylist(gui_cursor = playlist_cursor[:], playlist = song_playlist, menu_selected = None, list_of_instruments = playlist_list_of_instruments[:])
										
def main():
	appendInstrumentListWithEmpty(7)
	playlist_loop()


	

if __name__ == "__main__":
	main()
