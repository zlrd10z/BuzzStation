from threading import Thread
import time
from core.midi_and_sync import midi_output1
from core.midi_and_sync  import midi_output2and3
from core.midi_and_sync  import sync
from core.player_proc import SendToPlayer


# bytes used to communication with arduino:
stop_byte = bytes([244])
byte_midi_output_2 = bytes([245])
byte_midi_output_3 = bytes([246])

# This function creates list of hex numbers, 
# each hex number element coresponding to decimal index number
def create_tracker_volumes():
    tracker_volumes = {}
    for i in range(11):
        tracker_volumes[str(i)] = i
    for i in range(6):
        tracker_volumes[chr(65 + i)] = 11 + i
    return tracker_volumes

tracker_volumes = create_tracker_volumes()

convert_notechannel_to_bytes = lambda channel: bytes([143 + channel])

def convert_midi_vol_to_bytes(vol):
    midi_volume = int(10 + (vol - 1) * (127 - 10) / 7)
    midi_volume = bytes([midi_volume])
    return midi_volume

#converting volume from hex scale to 1-100 scale
def convert_tracker_volume(vol):
    vol = tracker_volumes[vol]
    vol = int((vol / 16) * 100)
    return vol

class NoteMidiConverter:
    def __init__(self):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.notes_to_midi_bytes = {}
        first_note = 36
        for i in range(1, 10):
            for note in notes:
                self.notes_to_midi_bytes[note + str(i)] = first_note
                first_note += 1
    
    def get_note_in_bytes(self, note):
        note_in_bytes = self.notes_to_midi_bytes[note]
        note_in_bytes = bytes([note_in_bytes])
        return note_in_bytes
    
def play_pattern(song_data, send_to_player, nmc, patt_output2n3_data, serial_usb):
    even = False
    def wait_for_next_quarter(song_data):
        nonlocal even
        time_between_quarters = song_data.get_data('time_between_quarter_notes')
        swing_to_time = time_between_quarters * (song_data.get_data('swing') / 100)
        if even:
            time_between_quarters -= swing_to_time
            even = False
        else:
            time_between_quarters += swing_to_time
            even = True
        time.sleep(time_between_quarters)

    def should_continue_playing(song_data):
        if song_data.get_data('is_playing') and not song_data.get_data('is_song_playing'):
            result = True
        else:
            result = False
        return result

    def play_drums(song_data, pattern_number, send_to_player):
        #for each quarter:
        for q in range(16):
            # Send sync signal through audio jack output:
            # get pattern for each note, so notes changes are possible while playing: 
            pattern = song_data.drums_pattern_operations('get pattern', pattern_number)
            # for max 16 samples:
            for s in range(16):
                if len(pattern[s][q]) > 0:
                    note = pattern[s][q]
                    # Volume
                    note_vol = convert_tracker_volume(note[1]) # convert hex to to number for int 0 - 100
                    sample_main_vol = (song_data.get_data('samples_volume')[s]) / 10
                    vol = (note_vol * sample_main_vol) / 100
                    sample_note = note[0]
                    if ' ' in sample_note:
                        sample_note = sample_note[:2]
                    send_to_player.play_note(s, sample_note, vol)
            sync.sync_out()
            if not should_continue_playing(song_data):
                break

            wait_for_next_quarter(song_data)
            if not should_continue_playing(song_data):
                send_to_player.stop_playing()
                break
    
    def play_midi(song_data, track_number, pattern_number, nmc, patt_output2n3_data, serial_usb):
        pattern = song_data.pianoroll_pattern_operations('get pattern for single track', track_number, pattern_number)
        pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get pattern for single track', 
                                                                           track = track_number, 
                                                                           pattern_number = pattern_number, 
                                                                           target_notes_to_turn_off = True
                                                                          )
        midi_ouput_channel = song_data.get_data('playlist_list_of_instruments')[track_number+1]
        midi_output = int(midi_ouput_channel[1])
        midi_channel = int(midi_ouput_channel[3:])
        midi_channel = convert_notechannel_to_bytes(midi_channel)
        for q in range(16):
            # Send sync signal through audio jack output:
            sync.sync_out()
            # If there is any note to play in quarter: 
            if len(pattern[q]) > 0:
                notes = pattern[q]
                for n in range(len(notes)):
                    note = notes[n]
                    note_in_bytes = nmc.get_note_in_bytes(note[0])
                    vol_in_bytes = convert_midi_vol_to_bytes(note[2])
                    midi_data = midi_channel + note_in_bytes + vol_in_bytes
                    if midi_output == 1:
                        midi_output1.send_data(midi_data)
                    else:
                        if midi_output == 2:
                            midi_data = byte_midi_output_2 + midi_data
                        elif midi_output == 3:
                            midi_data = byte_midi_output_3 + midi_data
                        patt_output2n3_data.append(midi_data)
                        
            if len(patt_output2n3_data) > 0:
                data_to_send = bytes([])
                for note_bytes in patt_output2n3_data:
                    data_to_send += note_bytes
                midi_output2and3.send_data_to_arduino(serial_usb, data_to_send)
                patt_output2n3_data.clear()

            #wait to next quarter:
            wait_for_next_quarter(song_data)
            # turn off notes:
            if len(pattern_notes_to_turn_off[q]) > 0:
                notes = pattern_notes_to_turn_off[q]
                for n in range(len(notes)):
                    note = notes[n]
                    note_in_bytes = nmc.get_note_in_bytes(note)
                    vol_in_bytes = bytes([0])
                    midi_data = midi_channel + note_in_bytes + vol_in_bytes
                    if midi_output == 1:
                        midi_output1.send_data(midi_data)
                    else:
                        if midi_output == 2:
                            midi_data = byte_midi_output_2 + midi_data
                        elif midi_output == 3:
                            midi_data = byte_midi_output_3 + midi_data
                        patt_output2n3_data.append(midi_data)



            if not should_continue_playing(song_data):
                midi_output1.all_notes_off()
                #247 - msg to arduino - all notes off byte
                midi_output2and3.send_data_to_arduino(serial_usb, bytes([247]), output=None) 
                break

    pattern_number = song_data.get_data('playing_pattern')
    track_number = song_data.get_data('playing_track')
    if track_number == 0:
        play_drums(song_data, pattern_number, send_to_player)
    else:
        track_number -= 1
        play_midi(song_data, track_number, pattern_number, nmc, patt_output2n3_data, serial_usb)

#goes thorug playlist and check on which level last pattern was added on the longest track:
def find_last_patt_lvl(playlist):
    last_pattern_index = None
    for track in range(len(playlist)):
        for pattern in range(len(playlist[track])-1, -1, -1):
            if playlist[track][pattern] != ' ':
                if last_pattern_index is None:
                    last_pattern_index = pattern
                    break
                else:
                    playlist[track][pattern] = int(playlist[track][pattern])
                    if playlist[track][pattern] > last_pattern_index:
                        last_pattern_index = playlist[track][pattern]
                        break
    return last_pattern_index

def play_song(song_data, send_to_player, nmc, song_output2n3_data, serial_usb):
    even = False
    def wait_for_next_quarter(song_data):
        nonlocal even
        time_between_quarters = song_data.get_data('time_between_quarter_notes')
        swing_to_time = time_between_quarters * (song_data.get_data('swing') / 100)
        if even:
            time_between_quarters -= swing_to_time
            even = False
        else:
            time_between_quarters += swing_to_time
            even = True
        time.sleep(time_between_quarters)

    playlist = song_data.get_data('song_playlist')
    instruments = song_data.get_data('playlist_list_of_instruments')
    even = False
    
    # The length of the playlist for each instrument can vary, then calculate which is the longest:
    last_pattern_index = find_last_patt_lvl(playlist)

    # If there is no pattern, don't do anything:
    if last_pattern_index == None: 
        return None
    start_playing_from = song_data.get_data('playing_song_from_lvl')
    # for each pattern in playlist for lonest track:
    for p in range(start_playing_from, last_pattern_index+1):
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
            sync.sync_out()
            for i in range(16):
                # AUDIO FILES:
                # first slot is for audio samples, rest are for midi instruments, so they are diffrently handled:
                if i == 0:
                    # for sample in quarter (16 slots for samples):
                    for s in range(16):
                        if drum_pattern is not None:
                            if len(drum_pattern[s][q]) > 0:
                                note = drum_pattern[s][q]
                                sample_speed = note[0]
                                if ' ' in sample_speed:
                                    sample_speed = sample_speed[:-1]
                                note_vol = convert_tracker_volume(note[1]) # convert hex to to number for int 0 - 16
                                sample_main_vol = (song_data.get_data('samples_volume')[s]) / 10
                                vol = (note_vol * sample_main_vol) / 100
                                send_to_player.play_note(s, sample_speed, vol)
                
                else:
                    # MIDI NOTES:
                    if i < len(playlist) and i < len(instruments):
                        if instruments[i] != 'Empty':
                            if p < len(playlist[i]):
                                midi_output_channel = instruments[i]
                                midi_output = int(midi_output_channel[1])
                                midi_channel = int(midi_output_channel[3:])
                                midi_channel = convert_notechannel_to_bytes(midi_channel)
                                notes = song_data.pianoroll_pattern_operations(operation = 'get notes', 
                                                                               track = i - 1, 
                                                                               pattern_number = playlist[i][p], 
                                                                               quarter = q
                                                                               )
                                # for each note notes in quarter:
                                if notes is not None:
                                    for n in range(len(notes)):
                                        note = notes[n]
                                        note_in_bytes = nmc.get_note_in_bytes(note[0])
                                        vol_in_bytes = convert_midi_vol_to_bytes(note[2])
                                        midi_data = midi_channel + note_in_bytes + vol_in_bytes
                                        if midi_output == 1:
                                            midi_output1.send_data(midi_data)
                                        else:
                                            if midi_output == 2:
                                                midi_data = byte_midi_output_2 + midi_data
                                            elif midi_output == 3:
                                                midi_data = byte_midi_output_3 + midi_data
                                            song_output2n3_data.append(midi_data)
            if len(song_output2n3_data) > 0:
                data_to_send = bytes([])
                for note_bytes in song_output2n3_data:
                    data_to_send += note_bytes
                midi_output2and3.send_data_to_arduino(serial_usb, data_to_send)
                song_output2n3_data.clear()

            # Stop Playing:
            if not song_data.get_data('is_playing') or not song_data.get_data('is_song_playing'):
                midi_output1.all_notes_off()
                #247 - msg to arduino - all notes off byte
                midi_output2and3.send_data_to_arduino(serial_usb, bytes([247]), output=None)
                send_to_player.stop_playing()
                break

            wait_for_next_quarter(song_data)
            
            # Turn off MIDI notes:
            for i in range(1, 17):
                if i < len(playlist) and i < len(instruments):
                    if instruments[i] != 'Empty':
                        if p < len(playlist[i]):
                            notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get notes', 
                                                                                       track = i - 1, 
                                                                                       pattern_number = playlist[i][p], 
                                                                                       quarter = q, 
                                                                                       target_notes_to_turn_off = True
                                                                                       )
                            midi_output_channel = instruments[i]
                            midi_output = int(midi_output_channel[1])
                            midi_channel = int(midi_output_channel[3:])
                            midi_channel = convert_notechannel_to_bytes(midi_channel)
                            if notes_to_turn_off is not None:
                                for note in notes_to_turn_off:
                                    note_in_bytes = nmc.get_note_in_bytes(note)
                                    vol_in_bytes = bytes([0])
                                    midi_data = midi_channel + note_in_bytes + vol_in_bytes
                                    if midi_output == 1:
                                        midi_output1.send_data(midi_data)
                                    else:
                                        if midi_output == 2:
                                            midi_data = byte_midi_output_2 + midi_data
                                        elif midi_output == 3:
                                            midi_data = byte_midi_output_3 + midi_data
                                        song_output2n3_data.append(midi_data)
            # Stop Playing: 
            if not song_data.get_data('is_playing') or not song_data.get_data('is_song_playing'):
                midi_output1.all_notes_off()
                #247 - msg to arduino - all notes off byte
                midi_output2and3.send_data_to_arduino(serial_usb, bytes([247]), output=None)
                send_to_player.stop_playing() 
                break

def main_loop(data_for_thread):
    song_output2n3_data = []
    patt_output2n3_data = []
    song_data = data_for_thread['song_data']
    queue_player = data_for_thread['queue_player']
    serial_usb = data_for_thread['serial_usb']
    send_to_player = SendToPlayer(queue_player)
    nmc = NoteMidiConverter()
    while True:
        if song_data.get_data('is_playing') and song_data.get_data('is_song_playing'):
            play_song(song_data, send_to_player, nmc, song_output2n3_data, serial_usb)
        elif song_data.get_data('is_playing') and not song_data.get_data('is_song_playing'):
            play_pattern(song_data, send_to_player, nmc, patt_output2n3_data, serial_usb)
        elif not song_data.get_data('is_playing') and not song_data.get_data('is_song_playing'):
            if len(song_output2n3_data) > 0:
                song_output2n3_data.clear()
            if len(patt_output2n3_data) > 0:
                patt_output2n3_data.clear()
        else:
            time.sleep(0.1)
        # check if song was was loaded by pickle / new song was creaated
        # if yes, then upload.
        if song_data != data_for_thread['song_data']:
            song_data = data_for_thread['song_data']

