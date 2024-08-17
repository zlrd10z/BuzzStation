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
clear = lambda: os.system("clear")
GUIplaylist = lambda cursor, playlist, menu_selected, first_note: gui_playlist.main(list_of_instruments = playlist_list_of_instruments,
										bpm_value = bpm,
										swing_value = swing,
										vol_value = bvol,
										playlist = playlist,
										cursor = cursor,
										menu_selected = menu_selected,
										first_number = first_note
										)

async def potentiometersOperations():
	while True:
		pots_values = potentiometers.returnPotentiometersValues()
		bpm = potentiometer_values_transform.bpmFromPotentiometer0(pots_values[0])
		swing = potentiometer_values_transform.swingFromPotentiometer1(pots_values[1])
		bvol = potentiometer_values_transform.volumeFromPotentiometer2(pots_values[2])
		timeBetweenQuarterNotes = potentiometer_values_transform.countTimePerQuarterNote(bpm)
		time.sleep(0.1)
		await asyncio.sleep(0.1) 

def saveSong():
	pass

def loadSong():
	pass

def playSong():
	pass


		
async def playlist_loop():
	global song_playlist
	def createEmptySongPlaylist():
		instrument = []
		for i in range(16):
			instrument.append(None)
		song_playlist.append(instrument)
	
	createEmptySongPlaylist()
		
	playlist_cursor = [0, 0]
	# Playlist loop:
	previous_printed_values = [None, None, None]
	
	while True:
		if playlist_cursor[1] > 16:
			first_note = playlist_cursor[1] % 16
			cursor = [playlist_cursor[0], playlist_cursor[1] % 16]
			if playlist_cursor[1] > len(song_playlist + 1):
				for i in range(len(song_playlist)):
					for j in range(16):
						song_playlist[i][j] = None
		else: 
			cursor = playlist_cursor
			first_note = 1
		
		
	
		
		if previous_printed_values[0] == cursor and previous_printed_values[1] == song_playlist and previous_printed_values[2] == first_note:
			#print(previous_printed_values[0], cursor)
			pass
		else:
			clear()
			GUIplaylist(cursor = cursor, playlist = song_playlist, menu_selected = None, first_note = first_note)
			previous_printed_values[0] = copy.deepcopy(cursor)
			previous_printed_values[1] = copy.deepcopy(song_playlist)
			previous_printed_values[2] = first_note
			
		key = keys.check_keys()
		if key != "":
			if key == '2':
				if playlist_cursor[1] > 0:
					playlist_cursor[1] -=  - 1
				
			if key == '8':
				playlist_cursor[1] += 1

			if key == '4':
				if playlist_cursor[0] > 0: 
					playlist_cursor[0] -= 1
			
			if key == '6':
				if playlist_cursor[0] <= len(playlist_list_of_instruments):
					playlist_cursor[0] += 1
					
			if key == '7':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if len(playlist_list_of_instruments) - 1 <= playlist_cursor[0]:
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) - 1 == 0:
							channel = 16
						else:
							channel = int(midi_instrument[3:]) - 1
						midi_instrument = midi_instrument[3:] + channel
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
				
			if key == '9':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					if len(playlist_list_of_instruments) - 1 <= playlist_cursor[0]:
						midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
						if int(midi_instrument[3:]) + 1 == 17:
							channel = 1
						else:
							channel = int(midi_instrument[3:]) + 1
						midi_instrument = midi_instrument[3:] + channel
						playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
			
			if key == '3':
				selected = 0
				while True:
					GUIplaylist(cursor = None, playlist = song_playlist, menu_selected = selected, first_note = 1)
					key = keys.check_keys()
					if key != "":
						if key == '4':
							if selected == 0:
								selected = 1
								
						if key == '6':
							if selected == 1:
								selected = 0
								
						if key == '5':
							if selected == 0:
								saveSong()
							else:
								loadSong()
							break
							
						if key == '1':
							break
			
			if key == '*':
				playSong()
				
			if key == '5':
				if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
					# Assign new midi output port to an empty slot:
					if len(playlist_list_of_instruments) - 1 > playlist_cursor[0]:
						playlist_list_of_instruments.append("M1c1")
						createEmptySongPlaylist()
					# Change midi output port
					else:
						midi_instrument = playlist_list_of_instruments(playlist_cursor[0])
						midi_channel = midi_instrument[3:]
						midi_output = int(midi_instrument[1])
						if midi_output == 3:
							midi_output = 1
						else:
							midi_output += 1
						playlist_list_of_instruments[playlist_cursor[0]] = "M" + str(midi_output) + midi_channel
		#await asyncio.sleep(0.1) 
													
async def main():
	task0 = asyncio.create_task(potentiometersOperations())
	task1 = asyncio.create_task(playlist_loop())
	await asyncio.gather(task0, task1)

	

if __name__ == "__main__":
	asyncio.run(main())
