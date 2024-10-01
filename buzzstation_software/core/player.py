import multiprocessing
from threading import Thread
import pygame
import time
from . import midi_output1
from . import midi_output2and3
from . import sync

# bytes used to communication with arduino:
stop_byte = bytes([221])
byte_midi_output_2 = bytes([222])
byte_midi_output_3 = bytes([223])


tracker_volumes = {}
for i in range(11):
	tracker_volumes[str(i)] = i

for i in range(6):
	tracker_volumes[chr(65 + i)] = 11 + i


def convert_channel_to_bytes(channel):
	channel = bytes([143 + channel])
	return channel

def convert_volume_to_bytes(vol):
	midi_volume = int(10 + (vol - 1) * (127 - 10) / 7)
	midi_volume = bytes([midi_volume])
	return midi_volume

def convert_tracker_volume(vol):
	vol = tracker_volumes[vol]
	vol = int((input_volume / 16) * 100)
	return vol
	

class NoteMidiConverter:
	def __init__(self):
		notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
		self.notes_to_midi_bytes = {}
		first_note = 36
		
		for i in range(6):
			for note in notes:
				self.notes_to_midi_bytes[note + str(i)] = first_note
				first_note += 1
	
	def get_note_in_bytes(self, note):
		note_in_bytes = self.notes_to_midi_bytes[note]
		note_in_bytes = bytes([note_in_bytes])
		return note_in_bytes
	

def player_audiofiles(child_conn):
	pygame.mixer.pre_init(44100, -16, 2, 16)
	pygame.mixer.init()
	pygame.mixer.set_num_channels(16)
	channels = [pygame.mixer.Channel(i) for i in range(16)]
	channel = 0
	samples = []
	for i in range(16):
		samples.append(None)

	
	while True:
		data = child_conn
		
		# Stop playing:
		if data = "stop":
			for channel in channels:
				channel.stop()
		
		# Update sample paths:
		elif "samples" in data:
			sample_number = child_conn
			sample_path = child_conn
			samples[sample_number] = pygame.mixer.Sound(sample_path)
		
		else:
			sample_number = data[0]
			vol = data[1]
			if samples[sample_number] is not None:
				channels[sample_number].set_volume(vol)
				channels[sample_number].play(samples[sample_number])
				
def player_pattern(track_number, pattern_number, data_storage, nmc, parent_conn):
	
	# If sample changed, send new sample to player in another process:
	if data_storage.get_data("last_changed_sample") is not None:
		parent_conn = "samples"
		parent_conn = data_storage.get_data("last_changed_sample")[1]
		parent_conn = data_storage.get_data("last_changed_sample")[0]
		data_storage.put_data("last_changed_sample", None)
	
	drum_pattern = data_storage.drums_pattern_operations(operation = "get pattern", 
															 pattern_number = pattern_number
															)

	if data_storage.pianoroll_pattern_operations("exists", pattern_number):
		midi_patterns = data_storage.pianoroll_pattern_operations(operation = "get_whole_pattern",
																  pattern_number = pattern_number
																 )
	else:
		midi_patterns = None
	
	midi_outputs_and_channels = data_storage.get_data("playlist_list_of_instruments")
	
	while True:
		#for each quarter note in pattern:
		for q in range(16):
			# send syncout signal via audio jack:
			sync.sync_out(True)
			
			if track_number == 0:
				#for each sample
				for s in range(16):
					if len(drum_pattern[q][s]) > 0:
						# play audio files samples:
						parent_conn = s
						parent_conn = convert_tracker_volume(drum_pattern[q][s][1])
						


			
			else:
				if midi_patterns is not None:
					for full_note_info in midi_patterns[track][q]:
						note = get_note_in_bytes(full_note_info[0])

						midi_output = midi_outputs_and_channels[track_number][1]


						channel = midi_outputs_and_channels[track_number][-3]
						convert_channel_to_bytes(channel)

						vol = nmc.convert_volume_to_bytes(full_note_info[2])

						if midi_output == 1:
							midi_output1.send_data(note[0], channel[0], vol[0])
						else:
							if midi_output == 2:
								midi_output = byte_midi_output_2
							else:
								midi_output = byte_midi_output_3

							midi_output2and3.sendDataToArduino(midi_output[0], note[0], channel[0], vol[0], stop_byte[0])

							track_number += 1


			
		
			# end of playing:
			if not data_storage.get_data("patternmode_is_song_playing") and not data_storage.get_data("is_playing"):
				midi_output2and3.turnOffAllNotesOnArduino()
				break
			
			time.sleep(int(data_storage.get_data("timeBetweenQuarterNotes") / 2))
			sync.sync_out(False)
			time.sleep(int(data_storage.get_data("timeBetweenQuarterNotes") / 2))
		
		# Playing in playlist mode (playling whole song without looping single pattern):
		if data_storage.get_data("patternmode_is_song_playing") and not data_storage.get_data("is_playing"):
			break
		# end of playing pattern in loop:
		elif not data_storage.get_data("patternmode_is_song_playing") and not data_storage.get_data("is_playing"):
			midi_output2and3.turnOffAllNotesOnArduino()
			parent_conn = "stop"
			break	
			
		
											
def song_player(data_storage, nmc, parent_conn):
	playlist = data_storage.get_data(song_playlist)
	
	for quarter in range(len(playlist[0])):
		for instrument in range(len(playlist)):
			if playlist[instrument][quarter] != " ":
				t = Thread(target=player_pattern, args=[instrument, playlist[instrument][quarter], data_storage, nmc, parent_conn])
				t.run()
		t.join() #wait for pattern to stop playing
	

def main(data_storage):
	nmc = NoteMidiConverter()
	parent_conn, child_conn = multiprocessing.Pipe()
	multiprocessing.Process(target=player_audiofiles, args=(child_conn,))
	
	while True:
		if data_storage.get_data("patternmode_is_song_playing"):
			song_player(data_storage, nmc, parent_conn)
		
		if data_storage.get_data("is_playing"):
			instrument = data_storage.get_data("instrument_played")
			player_pattern(instrument, pattern_number, data_storage, nmc, parent_conn)
		
		else:
			time.sleep(0.1)
		
