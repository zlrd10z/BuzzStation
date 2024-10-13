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

def create_tracker_volumes():
	tracker_volumes = {}
	for i in range(11):
		tracker_volumes[str(i)] = i

	for i in range(6):
		tracker_volumes[chr(65 + i)] = 11 + i
	return tracker_volumes
tracker_volumes = create_tracker_volumes()

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

# sending assigned midi instruments to channels via midi outputs:
def send_midi_instruments(song_data):
	channel = 191
	midi_instruments = song_data.get_data('playlist_list_of_midi_assigned')
	instruments = song_data.get_data('playlist_list_of_instruments')
	for i in range(1, len(midi_instruments)):
		midi_output_and_channel = instruments[i]
		midi_instrument = bytes([midi_instruments[instrument][1]])
		midi_output = midi_output_and_channel[1]
		midi_channel = midi_output_and_channel[3:]
		
		if midi_output = '1':
			midi_output1.send_data(bytes([191 + midi_channel, midi_instrument]))
		else
			if midi_output == '2':
				output = byte_midi_output_2
			elif midi_output == '3':
				output = byte_midi_output_3
			midi_output2and3.send_data_to_arduino(output + bytes([191 + midi_channel, midi_instrument] + stop_byte)
		
class NoteMidiConverter:
	def __init__(self):
		notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
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
		if data = 'stop':
			for channel in channels:
				channel.stop()
		# Update sample paths:
		elif 'sample' in data:
			sample_number = child_conn
			sample_path = child_conn
			samples[sample_number] = pygame.mixer.Sound(sample_path)
		elif 'samples' in data:
			sample_paths = child_conn
			for i in range(len(sample_paths)):
				if sample_paths[i] == 'Empty':
					samples[i] = None
				else:
					samples[i] = sample_paths[i]
		else:
			sample_number = data[0]
			vol = data[1]
			if samples[sample_number] is not None:
				channels[sample_number].set_volume(vol)
				channels[sample_number].play(samples[sample_number])

def play_pattern(song_data, track_number, pattern_number):
	even = False
	def wait_for_next_quarter(song_data):
		nonlocal even
		#time_between_quarters = song_data.get_data('time_between_quarter_notes')
		time_between_quarters = 0.1
		if even:
			time_between_quarters - song_data.get_data('swing')
			even = False
		else:
			time_between_quarters + song_data.get_data('swing')
			even = True

		time.sleep(time_between_quarters)
	
	def play_drums(song_data, pattern_number):
		#for each quarter:
		for q in range(16):
			# get pattern for each note, so notes changes are possible while playing: 
			pattern = song_data.drums_pattern_operations('get pattern', pattern_number)
			# for max 16 samples:
			for s in range(16):
				if len(pattern[s][q]) > 0:
					note = pattern[s][q]
			wait_for_next_quarter(song_data)
	
	def play_midi(song_data, track_number, pattern_number):
		#for each quarter:
		pattern = song_data.pianoroll_pattern_operations('get pattern for single track', track_number, pattern_number)
		pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get pattern for single track', 
																		   track = track_number, 
																		   pattern_number = pattern_number, 
																		   target_notes_to_turn_off = True
																		  )
		for q in range(16):
			# for max 16 samples:
			if len(pattern[q]) > 0:
				notes = pattern[q]
				
			wait_for_next_quarter(song_data)
			
			# turn off notes:
			if len(pattern_notes_to_turn_off[q]) > 0:
				notes = pattern_notes_to_turn_off[q]

	if track_number == 0:
		play_drums(song_data, pattern_number)
	else:
		track_number -= 1
		play_midi(song_data, track_number, pattern_number)

def play_song(song_data):
	playlist = song_data.get_data('song_playlist')
	instruments = song_data.get_data('playlist_list_of_instruments')
	even = False
	
	# The length of the playlist for each instrument can vary, then calculate which is the longest:
	longest_list = max(playlist, key=len)
	playlist_singletrack_index = playlist.index(longest_list)

	# for each pattern in playlist for lonest track:
	for p in range(len(playlist[playlist_singletrack_index])):
		# Get drums pattern:
		if p < len(playlist[0]):
			if(playlist[0][p] != ' '):
				drums_pattern_number = int(playlist[0][p])
				drum_pattern = song_data.drums_pattern_operations(operation = 'get pattern', pattern_number = drums_pattern_number)
			else:
				drum_pattern = None
				
		# for each quarter in pattern, 16 quarter notes per pattern:
		for q in range(16):
			# for each instrument (16 slots for instruments):
			for i in range(16):
				# first slot is for audio samples, rest are for midi instruments, so they are diffrently handled:
				if i == 0:
					# for sample in quarter (16 slots for samples):
					for s in range(16):
						if drum_pattern is not None:
							if len(drum_pattern[s][q]) > 0:
								note = drum_pattern[s][q]
				
				else:
					# MIDI note:
					if i < len(playlist):
						if p < len(playlist[i]):
							notes = song_data.pianoroll_pattern_operations(operation = 'get notes', track = i - 1, pattern_number = playlist[i][p], quarter = q)
			
			time_between_quarters = song_data.get_data('time_between_quarter_notes')
			if even:
				time_between_quarters - song_data.get_data('swing')
				even = False
			else:
				time_between_quarters + song_data.get_data('swing')
				even = True
			time.sleep(time_between_quarters)
			
			# Turn off MIDI notes:
			for i in range(1, 17):
					if i < len(playlist):
						if p < len(playlist[i]):
							notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get notes', 
																					   track = i - 1, 
																					   pattern_number = playlist[i][p], 
																					   quarter = q, 
																					   target_notes_to_turn_off = True
																					  )


def main(song_data):
	nmc = NoteMidiConverter()
	parent_conn, child_conn = multiprocessing.Pipe()
	multiprocessing.Process(target=player_audiofiles, args=(child_conn,))

	while True:
		if song_data.get_data('patternmode_is_song_playing'):
			song_player(song_data, nmc, parent_conn)
		if song_data.get_data('is_playing'):
			instrument = song_data.get_data('instrument_played')
			player_pattern(instrument, pattern_number, song_data, nmc, parent_conn)
		else:
			time.sleep(0.1)
		
