from libs.keypad import Keypad
from tui.tui_playlist import main as display_tui
from core import warning_window
from .song_data import SongData
import time
import copy
import pickle
from . import tracker
from . import pianoroll
from . import convert_audio_to_temp
from threading import Thread
from core.potentiometers_operations import pots_operations
from core.midi_params_menu import midi_menu
from core.player_proc import SendToPlayer
from core import player
from core.playlist_menu import menu 


def create_empty_song_playlist(song_data):
    song_playlist = song_data.get_data('song_playlist')
    track_for_instrument = []
    if len(song_playlist) == 0:
        n = 16
    else:
        # make it the same size as drums playlist
        n = len(song_playlist[0])
    for i in range(n):
        track_for_instrument.append(' ')
    song_playlist.append(track_for_instrument)
    song_data.put_data('song_playlist', song_playlist)

# This function check if any value from potentiometer, and if it's true, it's displaying new value on screen: 
def pots_values_tui(song_data, previous_printed_values, playlist_cursor, 
                    song_playlist, playlist_list_of_instruments, selection
):
    # Get potentiometers transformed data from data storage object:
    bpm = song_data.get_data('bpm')
    swing = song_data.get_data('swing')
    bvol = song_data.get_data('bvol')
    if previous_printed_values[0] != bpm or previous_printed_values[1] != swing or previous_printed_values[2] != bvol:
        display_tui(
                    song_data=song_data, 
                    list_of_instruments=playlist_list_of_instruments, 
                    tui_cursor=playlist_cursor[:], 
                    playlist=song_playlist,
                    selection=selection
                    )
        previous_printed_values[0] = bpm
        previous_printed_values[1] = swing    
        previous_printed_values[2] = bvol
    return previous_printed_values

def direction_keypad(key, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments):
    # keypad 2 and 8 are up and down keypad, keypad 4 and 6 are left and right keypad
    if key == '2':
        # Move cursor up:
        if playlist_cursor[1] > 0:
            playlist_cursor[1] -=  1
            song_data.put_data('playing_song_from_lvl', playlist_cursor[1]-1)

    if key == '8':
        # Move cursor down:
        if playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
            if playlist_cursor[0] < 15:
                playlist_cursor[1] += 1
                song_data.put_data('playing_song_from_lvl', playlist_cursor[1]-1)
        #create list with 
        if playlist_cursor[1] > len(song_playlist[0]):
            for i in range(len(song_playlist)):
                for j in range(16):
                    song_playlist[i].append(' ')
    if key == '4':
        # Move cursor left:
        if playlist_cursor[0] > 0: 
            playlist_cursor[0] -= 1
        elif playlist_cursor[0] == 0:
            # jump to firs from right added instrument:
            playlist_cursor[0] = len(song_playlist) - 1
    if key == '6':
        # move cursor right
        if playlist_cursor[0] == 15:
            playlist_cursor[0] = 0
        # Move cursor to next Empty instrument only when instrument on which cursor points to is not empty:
        elif playlist_list_of_instruments[playlist_cursor[0]] != 'Empty' and playlist_cursor[1] == 0:
            playlist_cursor[0] += 1
            # if cursor will point to instrument that is not in playlist_list_of_instruments, add more empty to not exceed list length:
            if playlist_cursor[0] + 1 == len(playlist_list_of_instruments):
                for i in range(8): 
                    playlist_list_of_instruments.append('Empty')   
        # Move cursor on playlist to next intrument, only if it's not Empty:
        elif playlist_list_of_instruments[playlist_cursor[0] + 1] != 'Empty' and playlist_cursor[1] != 0:
            playlist_cursor[0] += 1
    return playlist_cursor

#EDIT key - key with [E] sticker on it:
def edit_key(keypad, song_data, playlist_cursor, song_playlist, data_for_threads):
    playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
    if playlist_cursor[1]-1 < 0:
        pattern_number_for_tracker = None
    else:
        pattern_number_for_tracker = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
    while True:
        # Select new midi instrument for midi output:
        if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
            midi_output = song_data.get_data('playlist_list_of_instruments')[playlist_cursor[0]]
            if midi_output == 'Empty':
                midi_output = 'M1c1'
                midi_instruments = song_data.get_data('playlist_list_of_instruments')
                midi_instruments[playlist_cursor[0]] = midi_output
                midi_instruments = song_data.put_data('playlist_list_of_instruments', midi_instruments)  
            midi_instruments = song_data.get_data('playlist_list_of_midi_assigned')
            midi_instrument = midi_instruments[midi_output]
            midi_menu.main(keypad, song_data, midi_output, midi_instrument, playlist_cursor[0])
        if pattern_number_for_tracker is None or pattern_number_for_tracker == ' ':
                break
        if playlist_cursor[0] == 0:
            pattern_number_for_tracker = tracker.main(keypad, song_data, pattern_number_for_tracker, data_for_threads)
        elif playlist_cursor[0] > 0 and playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
            pattern_number_for_tracker = pianoroll.main(
                                                          keypad = keypad, 
                                                          song_data = song_data,
                                                          pattern_number = pattern_number_for_tracker,
                                                          midi_and_channel = playlist_list_of_instruments[playlist_cursor[0]],
                                                          track = playlist_cursor[0] - 1
                                                       )

#keypad with [+] and [-] sticker - changing selected values:
def plus_n_minus_keypad(key, playlist_cursor, song_data, song_playlist, playlist_list_of_instruments):
    def minus(playlist_cursor, song_data, song_playlist, playlist_list_of_instruments):
        result = None
        # Toggle down midi instrument channel:
        if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
            if playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
                midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
                if int(midi_instrument[3:]) - 1 == 0:
                    channel = 16
                else:
                    channel = int(midi_instrument[3:]) - 1
                midi_instrument = midi_instrument[:3] + str(channel)
                playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
                result = ('playlist_list_of_instruments', playlist_list_of_instruments)
        # Change selected pattern to previous pattern (eg. from pattern 2 to pattern 1):
        elif playlist_cursor[1] != 0:
            # Remove pattern from a field:
            if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] == '1':
                song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = ' '
            # toggle down pattern:    
            else:
                if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] != ' ':
                    patt_number = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
                    patt_number = int(patt_number) 
                    if patt_number > 1:
                        patt_number -= 1
                    song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = patt_number
                    song_data.last_added(
                                         target = 'playlist', 
                                         track = playlist_cursor[0], 
                                         new_value = patt_number
                                         )
                    result = ('playlist', song_playlist)
        return result
    
    def plus(playlist_cursor, song_data, song_playlist, playlist_list_of_instruments):
        result = None
        # Toggle up midi instrument channel:
        if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
            if playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
                midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
                if int(midi_instrument[3:]) + 1 == 17:
                    channel = 1
                else:
                    channel = int(midi_instrument[3:]) + 1
                midi_instrument = midi_instrument[:3] + str(channel)
                playlist_list_of_instruments[playlist_cursor[0]] = midi_instrument
            result = ('playlist_list_of_instruments', playlist_list_of_instruments)
        # Change selected pattern to previous pattern (eg. from pattern 1 to pattern 2):
        elif playlist_cursor[1] != 0:
            # Add pattern to an empty field:
            if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] == ' ':
                song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = '1'
            # toggle down pattern:    
            else:
                if song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] != ' ':
                    patt_number = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
                    patt_number = int(patt_number) + 1
                    song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = patt_number
                    song_data.last_added(
                                         target = 'playlist', 
                                         track = playlist_cursor[0], 
                                         new_value = patt_number
                                         )
            result = ('playlist', song_playlist)
        return result
    
    if key == '7':
        result = minus(playlist_cursor, song_data, song_playlist, playlist_list_of_instruments)
    if key == '9':
        result = plus(playlist_cursor, song_data, song_playlist, playlist_list_of_instruments)
    
    return result

# Key with [C] sticker on it:
def clear_key(keypad, screen_matrix, song_playlist, playlist_cursor):
    ok_selected = warning_window.main(keypad, screen_matrix, 'clear track')
    if ok_selected:     
        for i in range(len(song_playlist[playlist_cursor[0]])):
            song_playlist[playlist_cursor[0]][i] = ' ' 
    return song_playlist

def play_pause(song_data):
    playing = song_data.get_data('is_playing')
    playing_song = song_data.get_data('is_song_playing')
    if not playing and not playing_song:
        song_data.put_data('is_playing', True)
        song_data.put_data('is_song_playing', True)
        result = True
    else:
        song_data.put_data('is_playing', False)
        song_data.put_data('is_song_playing', False)
        result = False
    return result

'''
start_xy_get:
When a user in the menu puts the copy start flag somewhere, e.g. lvl 3 of Track Drums, 
and his cursor is at lvl 10, he can use the copy function to copy the pattern arrangement 
from lvl 3 to lvl 9 and paste it at a different location of his choice.
This var will store that inforamtion.
'''
class Selection():
    def __init__(self):
        self.__sel_start_xy = None
        self.__sel_end_xy = None

    def get(self, var_name):
        return getattr(self, f'_{self.__class__.__name__}__{var_name}')

    def update(self, var_name, new_value):
        setattr(self, f'_{self.__class__.__name__}__{var_name}', new_value)

class Undo():
    def __init__(self):
        self.prev_data = None

    def put(self, data):
        self.prev_data = copy.deepcopy(data)

    def get(self):
        return self.prev_data


def main(keypad, song_data, data_for_threads):
    create_empty_song_playlist(song_data)
    selection = Selection()
    previous_printed_values = [0, 0, 0]
    undo = Undo()
    # Playlist loop:
    while True:
        # Get lists from data storage:
        playlist_cursor = song_data.get_data('playlist_cursor')
        song_playlist = song_data.get_data('song_playlist')
        playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
        
        # Update screen, if any value from potentiometers has changed:
        previous_printed_values = pots_values_tui(
                                                  song_data, previous_printed_values, 
                                                  playlist_cursor, song_playlist, 
                                                  playlist_list_of_instruments, selection
                                                  )
        # Get key from keypad:    
        key = keypad.check_keys()
        if key != '':
            # keypad 2 and 8 are up and down keypad, keypad 4 and 6 are left and right keypad
            if key == '2' or key == '4' or key == '6' or key == '8':
                playlist_cursor = direction_keypad(key, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments)   
            # Key with [E] sticker on it - edit selected pattern:
            elif key == '3':
                song_playlist = song_data.get_data('song_playlist')
                edit_key(keypad, song_data, playlist_cursor, song_playlist, data_for_threads)
                playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
            # keypad with [+] and [-] sticker - changing selected values:    
            elif key == '7' or key == '9':
                result = plus_n_minus_keypad(key, playlist_cursor, song_data, song_playlist, playlist_list_of_instruments)
                if result is not None:
                    if result[0] == 'playlist':
                        playlist = result[1]
                    else:
                        playlist_list_of_instruments = result[1]
            # key [esc]: play playlist from first lvl:
            elif key == '1':
                song_data.put_data('playing_song_from_lvl', 0)
            # Key with [C] sticker - clear track on which cursor is present:
            elif key == '0':
                # get currently displayed GUI:
                screen_matrix = display_tui(
                                            song_data=song_data, 
                                            list_of_instruments=playlist_list_of_instruments, 
                                            tui_cursor=playlist_cursor[:], 
                                            playlist=song_playlist,
                                            selection=selection,
                                            printtui=False
                                            )

                song_playlist = clear_key(keypad, screen_matrix, song_playlist, playlist_cursor)
            # Key with [M] sticker - menu:
            elif key == '#':
                # Enter menu to save or load song or to clear entinre playlist:
                menu_return = menu(
                                   keypad, display_tui, song_data, playlist_cursor[:], 
                                   song_playlist, playlist_list_of_instruments,
                                   data_for_threads, selection, undo
                                  )
                if menu_return is not None:
                    if menu_return[0] == 'song_data':
                        song_data = menu_return[1]
                        song_playlist = song_data.get_data('song_playlist')
                        playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
                        playlist_cursor = [0, 0] 
                        display_tui(
                                    song_data=song_data, 
                                    list_of_instruments=playlist_list_of_instruments, 
                                    tui_cursor=playlist_cursor[:], 
                                    playlist=song_playlist,
                                    selection=selection
                                    )
                    elif menu_return[0] == 'playlist':
                        song_playlist = menu_return[1]
                    elif menu_return[0] == 'playlist cursor':
                        playlist_cursor = menu_return[1]

            # play button:
            elif key == '*':
                play_pause(song_data)
            # accept key:
            elif key == '5':
                if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
                    # Assign new midi output port to an empty instrument slot:
                    if playlist_list_of_instruments[playlist_cursor[0]] == 'Empty':
                        playlist_list_of_instruments[playlist_cursor[0]] = 'M1c1'
                        create_empty_song_playlist(song_data)
                        song_playlist = song_data.get_data('song_playlist')
                    # Change midi output port, if instrument slot is not empty:
                    elif playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
                        midi_instrument = playlist_list_of_instruments[playlist_cursor[0]]
                        midi_channel = midi_instrument[2:]
                        midi_output = int(midi_instrument[1])
                        if midi_output == 3:
                            midi_output = 1
                        else:
                            midi_output += 1
                        playlist_list_of_instruments[playlist_cursor[0]] = 'M' + str(midi_output) + midi_channel
                # Add of delete pattern on selected field:
                elif playlist_cursor[1]  != 0:
                    # Add last picked pattern (pattern picking with buttons [7] and [9]:
                    if song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] == ' ':
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = song_data.last_added('playlist', playlist_cursor[0])
                    # delete pattern:    
                    else:
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = ' '
            
            # when key was pressed, update displayed GUI:
            display_tui(
                        song_data=song_data, 
                        list_of_instruments=playlist_list_of_instruments, 
                        tui_cursor=playlist_cursor[:], 
                        playlist=song_playlist,
                        selection=selection
                        )
            #print(playlist_cursor)        

        # Update values in data storage:
        song_data.put_data('playlist_cursor', playlist_cursor)
        song_data.put_data('song_playlist', song_playlist)
        song_data.put_data('playlist_list_of_instruments', playlist_list_of_instruments)

if __name__ == '__main__':
    playlist_loop()
