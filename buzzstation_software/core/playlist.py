from libs.keypad import Keypad
from gui import gui_playlist, gui_warning_window
from .song_data import SongData
import time
import os
import copy
import pickle
from . import tracker
from . import pianoroll
from . import pick_file
from . import pick_midi_instrument
from . import convert_audio_to_temp


# Lambdas:
clear_screen = lambda: os.system('clear')
gui_playlist = lambda gui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname: gui_playlist.main(
                                list_of_instruments=list_of_instruments,
                                bpm_value=bpm,
                                swing_value=swing,
                                vol_value=bvol,
                                playlist=playlist,
                                gui_cursor=gui_cursor,
                                menu_selected=menu_selected,
                                songname=songname
                                )

gui_get_screen_matrix = lambda  gui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname: gui_playlist.main(
                                list_of_instruments= list_of_instruments,
                                bpm_value=bpm,
                                swing_value=swing,
                                vol_value=bvol,
                                playlist=playlist,
                                gui_cursor=gui_cursor,
                                menu_selected=menu_selected,
                                songname=songname,
                                printgui=False
                                )


# Remove all temporary audio files from .temp directory:
def clear_temp():
    cwd = os.getcwd()
    command = 'rm ' + cwd + '/.temp/* -f'
    os.system(command)

def save_song(song_data, keys):
    path_to_file = pick_file.get_filename('save song', keys)
    song_name = path_to_file.split('/')[-1]
    song_data.put_data('song_name', song_name)
    should_save_song = True
    # Check if file already exist, then ask user, if he wants to overwrite it:
    if path_to_file is not None:
        if os.path.isfile(path_to_file):
            ok_selected = False
            screen_matrix = []
            line = []
            for i in range(64):
                line.append(' ')
            for i in range(17):
                screen_matrix.append(line[:])
            for i in range(len(path_to_file)):
                screen_matrix[0][i] = path_to_file[i]
            # Warning window to prevent unintentional overwrite:
            gui_warning_window.main(screen_matrix, ok_selected, 'overwrite song')
            while True:
                key = keys.check_keys()
                if key != '':
                    if key == '4': ok_selected = True
                    if key == '6':     ok_selected = False
                    if key == '5':
                        if not ok_selected: should_save_song = False
                        else:
                            os.remove(path_to_file)
                            break
                    clear_screen()
                    gui_warning_window.main(screen_matrix, ok_selected, 'overwrite song')
    if should_save_song and path_to_file is not None:
        with open(path_to_file, 'wb') as file_btp:
            pickle.dump(song_data, file_btp)

def load_song(song_data, keys):
    path_to_file = pick_file.get_filename('load song', keys)
    if path_to_file is not None:
        with open(path_to_file, 'rb') as file_btp:
            song_data = pickle.load(file_btp)
        clear_temp()
        # Create temporary audio files adjusted for pygame mixer settings:
        samples = song_data.get_data('samples')
        for sample in samples:
            if sample != 'Empty':
                convert_audio_to_temp.convert_to_pygame_format(sample)
        # Set song loaded flag for True, this flag is used for update samples list in player in another process
        song_data.put_data('song_loaded', True)
        return song_data

def create_empty_song_playlist(song_data):
    song_playlist = song_data.get_data('song_playlist')
    track_for_instrument = []
    for i in range(16):
        track_for_instrument.append(' ')
    song_playlist.append(track_for_instrument)
    song_data.put_data('song_playlist', song_playlist)

#If there is nothing saved after the first 16 fields, delete after 16 fields the rest of the playlist consisting of empty characters to save memory:
def shorten_playlist_if_possible(playlist):
    # Check if playlist can be shorten:
    for i in range(len(playlist)):
        can_be_shorten = True
        for j in range(16):
            if playlist[i][len(playlist) - 1 - j] != ' ':
                can_be_shorten = False
        # Cut last 16 empty fields:
        if can_be_shorten:
            for i in range(len(playlist)):
                playlist[i] = playlist[i][:-16]
                
        return playlist

# This function check if any value from potentiometer, and if it's true, it's displaying new value on screen: 
def pots_values_gui(song_data, previous_printed_values, playlist_cursor, 
                    song_playlist, playlist_list_of_instruments,
):
    # Get potentiometers transformed data from data storage object:
    bpm = song_data.get_data('bpm')
    swing = song_data.get_data('swing')
    bvol = song_data.get_data('bvol')
    if previous_printed_values[0] != bpm or previous_printed_values[1] != swing or previous_printed_values[2] != bvol:
        clear_screen()
        gui_playlist(gui_cursor = playlist_cursor[:], 
                    playlist = song_playlist, 
                    menu_selected = None, 
                    list_of_instruments = playlist_list_of_instruments, 
                    bpm = bpm, 
                    swing = swing, 
                    bvol = bvol,
                    songname = song_data.get_data('song_name')
                   )
        previous_printed_values[0] = bpm
        previous_printed_values[1] = swing    
        previous_printed_values[2] = bvol
    return previous_printed_values

def direction_keys(key, playlist_cursor, song_playlist, playlist_list_of_instruments):
    # Keys 2 and 8 are up and down keys, keys 4 and 6 are left and right keys
    if key == '2':
        # Move cursor up:
        if playlist_cursor[1] > 0:
            playlist_cursor[1] -=  1
            if playlist_cursor[1] < (len(song_playlist[0]) -1) - 16:
                song_playlist = shorten_playlist_if_possible(song_playlist)
    if key == '8':
        # Move cursor down:
        if playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
            if playlist_cursor[0] < 15:
                playlist_cursor[1] += 1
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
        if playlist_cursor[0] + 1 == len(playlist_list_of_instruments):
            # if cursor point to instrument that is not in playlist_list_of_instruments, add more empty to not exceed list length:
            for i in range(8): playlist_list_of_instruments.append('Empty')
        elif playlist_cursor[0] == 15:
            playlist_cursor[0] = 0
        # Move cursor to next Empty instrument only when instrument on which cursor points to is not empty:
        elif playlist_list_of_instruments[playlist_cursor[0]] != 'Empty' and playlist_cursor[1] == 0:
            playlist_cursor[0] += 1
        # Move cursor on playlist to next intrument, only if it's not Empty:
        elif playlist_list_of_instruments[playlist_cursor[0] + 1] != 'Empty' and playlist_cursor[1] != 0:
            playlist_cursor[0] += 1
    return playlist_cursor

#EDIT key - key with [E] sticker on it:
def edit_key(song_data, playlist_cursor):
    if playlist_cursor[1]-1 < 0:
        pattern_number_for_tracker = None
    else:
        pattern_number_for_tracker = song_playlist[playlist_cursor[0]][playlist_cursor[1]-1]
    while True:
        # Select new midi instrument for midi output:
        if playlist_cursor[0] != 0 and playlist_cursor[1] == 0:
            midi_output = song_data.get_data('playlist_list_of_instruments')[playlist_cursor[0]]
            if midi_output != 'Empty':
                midi_instruments = song_data.get_data('playlist_list_of_midi_assigned')
                midi_instrument = midi_instruments[midi_output][0]
                choosen_instrument = pick_midi_instrument.main(keys, midi_output, midi_instrument)
                if choosen_instrument is not None:
                    midi_instruments[midi_output] = choosen_instrument
                    song_data.put_data('playlist_list_of_midi_assigned', midi_instruments)
                break
        if pattern_number_for_tracker is None or pattern_number_for_tracker == ' ':
                break
        if playlist_cursor[0] == 0:
            pattern_number_for_tracker = tracker.main(keys, song_data, pattern_number_for_tracker)
        elif playlist_cursor[0] > 0 and playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
            pattern_number_for_tracker = pianoroll.main(keypad = keys, 
                                                          song_data = song_data,
                                                          pattern_number = pattern_number_for_tracker,
                                                          midi_and_channel = playlist_list_of_instruments[playlist_cursor[0]],
                                                          track = playlist_cursor[0] - 1
                                                       )

#Keys with [+] and [-] sticker - changing selected values:
def plus_n_minus_keys(key, playlist_cursor, song_data, song_playlist):
    def minus(playlist_cursor, song_data, song_playlist):
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
                    patt_number = int(patt_number) - 1
                    song_playlist[playlist_cursor[0]][playlist_cursor[1]-1] = patt_number
                    song_data.put_data('last_added_pattern_numer', patt_number)
                    result = ('playlist', song_playlist)
        return result
    
    def plus(playlist_cursor, song_data, song_playlist):
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
                    song_data.put_data('last_added_pattern_numer', patt_number)
                    result = ('playlist', song_playlist)
        return result
    
    if key == '7':
        result = minus(playlist_cursor, song_data)
    if key == '9':
        result = plus(playlist_cursor, song_data)
    
    return result

# Key with [C] sticker on it:
def clear_key(keys, screen_matrix, song_playlist, playlist_cursor):
    ok_selected = False
    clear_screen()
    gui_warning_window.main(screen_matrix, ok_selected, 'clear song')
    while True:
        key = keys.check_keys()
        if key != '':
            if key == '4':
                ok_selected = True                    
            elif key == '6':
                ok_selected == False
            elif key == '1': 
                break
            elif key == '5':
                if ok_selected:
                    for i in range(len(song_playlist[playlist_cursor[0]])):
                        song_playlist[playlist_cursor[0]][i] = ' ' 
                    break
                else:
                    break

            clear_screen()    
            gui_warning_window.main(screen_matrix, ok_selected, 'clear song')
    return song_playlist

def menu_accept_key(keys, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments, selected):
    screen_matrix = gui_get_screen_matrix(gui_cursor=playlist_cursor[:], 
                                playlist=song_playlist, 
                                menu_selected=None, 
                                list_of_instruments=playlist_list_of_instruments, 
                                bpm=song_data.get_data('bpm'),
                                swing=song_data.get_data('swing'), 
                                bvol=song_data.get_data('bvol'),
                                songname=song_data.get_data('song_name')
                               )
    # Accept choice:
    if selected == 0:
        # Save song:
        save_song(song_data, keys)
        clear_screen()
        gui_playlist(gui_cursor=playlist_cursor[:], 
                    playlist=song_playlist, 
                    menu_selected=selected, 
                    list_of_instruments=playlist_list_of_instruments, 
                    bpm=song_data.get_data('bpm'),
                    swing=song_data.get_data('swing'), 
                    bvol=song_data.get_data('bvol'),
                    songname=song_data.get_data('song_name')
                    )
        break
    elif selected > 0:
        if selected == 1:
            warning_text = 'load song'
        if selected == 2:
            warning_text = 'new song'
        if selected == 3:
            warning_text = 'clear all tracks'

        ok_selected = False
        clear_screen()
        gui_warning_window.main(screen_matrix, ok_selected, warning_text)
        while True:
            key = keys.check_keys()
            if key != '':
                # dir key - left:
                if key == '4':
                    ok_selected = True
                # dir key - right:
                if key == '6':
                    ok_selected = False
                # [esc] key:
                if key == '1': break
                # [insert] key - accept key:
                if key == '5':
                    if ok_selected:
                        if selected == 1:
                            # Load Song
                            song_data = load_song(song_data, keys)
                        elif selected == 2:
                            #new song: clear all previous data
                            song_data = SongData()
                            create_empty_song_playlist(song_data)
                        elif selected == 3:
                            # Clear entire playlist:
                            song_playlist = song_data.get_data('song_playlist')
                            track_for_instrument = []
                            for i in range(16):
                                track_for_instrument.append(' ')
                            for i in range(len(song_playlist)):
                                song_playlist[i] = track_for_instrument[:]
                            song_data.put_data('song_playlist', song_playlist)
                        return song_data
                    # if [no] selected on the screen by user, abort:
                    else:
                        break
                clear_screen()
                gui_warning_window.main(screen_matrix, ok_selected, warning_text)    


# Enter menu to save or load song:
def menu(keys, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments):    
    selected = 0
    menu_cursor = [0, 0]
    clear_screen()
    gui_playlist(gui_cursor=playlist_cursor[:], 
                playlist=song_playlist, 
                menu_selected=selected, 
                list_of_instruments=playlist_list_of_instruments, 
                bpm=song_data.get_data('bpm'),
                swing=song_data.get_data('swing'), 
                bvol=song_data.get_data('bvol'),
                songname=song_data.get_data('song_name')
               )    
    while True:
        key = keys.check_keys()
        if key != '':
            previous_selected = selected
            # direction key - left:
            if key == '4':
                if menu_cursor[1] == 1:
                    menu_cursor[1] = 0
            # direction key - right:
            elif key == '6':
                if menu_cursor[1] == 0:
                    menu_cursor[1] = 1
            # direction key - up:
            elif key == '2':
                if menu_cursor[0] - 1 > -1:
                    menu_cursor[0] -= 1
            # direction key - down:
            elif key == '8':
                if menu_cursor[0] + 1 < 4:
                    menu_cursor[0] += 1    
            # esc key or menu key:
            elif key == '1' or key == '#':
                # Exit menu:
                break
            # accept key:
            if key == '5':
                new_song_data = menu_accept_key(keys, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments, selected)
                if new_song_data is not None:
                    return new_song_data
                
            # Get button selected on screen:
            if menu_cursor[0] == 0:
                if menu_cursor[1] == 0:
                    selected = 0
                else:
                    selected = 1
            if menu_cursor[0] == 1:
                    selected = 2
            if menu_cursor[0] == 2:
                    selected = 3

            # Check if selected button changed and displayit to user:
            if previous_selected != selected:
                clear_screen()
                gui_playlist(gui_cursor=playlist_cursor[:], 
                            playlist=song_playlist, 
                            menu_selected=selected, 
                            list_of_instruments=playlist_list_of_instruments, 
                            bpm=song_data.get_data('bpm'),
                            swing=song_data.get_data('swing'), 
                            bvol=song_data.get_data('bvol'),
                            songname=song_data.get_data('song_name')
                            )
                previous_selected = selected 

def play_pause(song_data):
    playing = song_data.get_data('is_playing')
    playing_song = song_data.get_data('is_song_playing')
    if not playing and not playing_song:
        song_data.put_data('is_playing', True)
        song_data.put_data('is_song_playing', True)
    else:
        song_data.put_data('is_playing', False)
        song_data.put_data('is_song_playing', False)

def pause(song_data):
    song_data.put_data('is_playing', False)
    song_data.put_data('is_song_playing', False)
    
def main(keys, song_data):
    create_empty_song_playlist(song_data)
    previous_printed_values = [0, 0, 0]
    # Playlist loop:
    while True:
        # Get lists from data storage:
        playlist_cursor = song_data.get_data('playlist_cursor')
        song_playlist = song_data.get_data('song_playlist')
        playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
        
        # Update screen, if any value from potentiometers has changed:
        previous_printed_values = pots_values_gui(song_data, previous_printed_values, 
                                                  playlist_cursor, song_playlist, playlist_list_of_instruments
                                                  )
        # Get key from keypad:    
        key = keys.check_keys()
        if key != '':
            # Keys 2 and 8 are up and down keys, keys 4 and 6 are left and right keys
            if key == '2' or key == '4' or key == '6' or key == '8':
                playlist_cursor = direction_keys(key, playlist_cursor, song_playlist, playlist_list_of_instruments)        
            # Key with [E] sticker on it - edit selected pattern:
            elif key == '3':
                edit_key(song_data, playlist_cursor)
            # Keys with [+] and [-] sticker - changing selected values:    
            elif key == '7' or key == '9':
                result = plus_n_minus_keys(key, playlist_cursor, song_data, song_playlist):
                if result[0] == 'playlist':
                    playlist = result[1]
                else:
                    playlist_list_of_instruments = result[1]
            # Key with [C] sticker - clear track on which cursor is present:
            elif key == '0':
                # get currently displayed GUI:
                screen_matrix = gui_get_screen_matrix(gui_cursor=playlist_cursor[:], 
                                                        playlist=song_playlist, 
                                                        menu_selected=None, 
                                                        list_of_instruments=playlist_list_of_instruments, 
                                                        bpm=bpm, 
                                                        swing=swing, 
                                                        bvol=bvol,
                                                        songname=song_data.get_data('song_name')
                                                       )
                song_playlist = clear_key(keys, screen_matrix, song_playlist, playlist_cursor)
            # Key with [M] sticker - menu:
            elif key == '#':
                # Enter menu to save or load song or to clear entinre playlist:
                new_song_data = menu(keys, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments, selected)
                if new_song_data is not None:
                    song_data = new_song_data
                    song_playlist = song_data.get_data('song_playlist')
                    playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
                    playlist_cursor = [0, 0]
                    clear_screen()
                    gui_playlist(gui_cursor=playlist_cursor[:], 
                                playlist=song_playlist, 
                                menu_selected=selected, 
                                list_of_instruments=playlist_list_of_instruments, 
                                bpm=song_data.get_data('bpm'),
                                swing=song_data.get_data('swing'), 
                                bvol=song_data.get_data('bvol'),
                                songname=song_data.get_data('song_name')
                                )
            # play button:
            if key == '*':
                play_pause(song_data)
            # accept key:
            if key == '5':
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
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = song_data.get_data('last_added_pattern_numer')
                    # delete pattern:    
                    else:
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = ' '
            
            # when key was pressed, update displayed GUI:
            clear_screen()
            gui_playlist(gui_cursor = playlist_cursor[:], 
                        playlist = song_playlist, 
                        menu_selected = None, 
                        list_of_instruments = playlist_list_of_instruments, 
                        bpm = bpm, 
                        swing = swing, 
                        bvol = bvol,
                        songname = song_data.get_data('song_name')
                       )    
        
        # Update values in data storage:
        song_data.put_data('playlist_cursor', playlist_cursor)
        song_data.put_data('song_playlist', song_playlist)
        song_data.put_data('playlist_list_of_instruments', playlist_list_of_instruments)

if __name__ == '__main__':
    playlist_loop()
