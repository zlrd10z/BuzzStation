from libs.keypad import Keypad
from tui import tui_playlist
from core import warning_window
from .song_data import SongData
import time
import os
import copy
import pickle
from . import tracker
from . import pianoroll
from . import pick_file
from . import convert_audio_to_temp
from threading import Thread
from core.potentiometers_operations import pots_operations
from core.midi_params_menu import midi_menu
from core.player_proc import SendToPlayer
from core import player
from tui import load_scrn


# Lambdas:
clear_screen = lambda: os.system('clear')
tui_pl = lambda tui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname, is_playing: tui_playlist.main(
                                list_of_instruments=list_of_instruments,
                                bpm_value=bpm,
                                swing_value=swing,
                                vol_value=bvol,
                                playlist=playlist,
                                tui_cursor=tui_cursor,
                                menu_selected=menu_selected,
                                songname=songname,
                                is_playing=is_playing
                                )

tui_get_screen_matrix = lambda  tui_cursor, playlist, menu_selected, list_of_instruments, bpm, swing, bvol, songname, is_playing: tui_playlist.main(
                                list_of_instruments= list_of_instruments,
                                bpm_value=bpm,
                                swing_value=swing,
                                vol_value=bvol,
                                playlist=playlist,
                                tui_cursor=tui_cursor,
                                menu_selected=menu_selected,
                                songname=songname,
                                printtui=False,
                                is_playing=is_playing
                                )


# Remove all temporary audio files from .temp directory:
def clear_temp():
    cwd = os.getcwd()
    command = 'rm ' + cwd + '/.temp/* -f'
    os.system(command)

# Convert samples to different speed according to their note which exist in patterns
def convert_non_defaults(song_data):
    load_scrn.draw()
    sample_paths = song_data.get_data('samples')
    samples_not_c5 = song_data.get_data('samples_not_c5')
    # for each sample/track
    for s in range(len(sample_paths)):
        if sample_paths[s] != 'Empty':
            #for each note that appears in patterns for that track:
            notes = [*samples_not_c5[s]]
            for n in range(len(notes)):
                convert_audio_to_temp.convert_to_pygame_format(sample_paths[s], notes[n])

def save_song(song_data, keypad):
    path_to_file = pick_file.get_filename('save song', keypad)
    should_save_song = False
    if path_to_file is not None:
        song_name = path_to_file.split('/')[-1]
        song_data.put_data('song_name', song_name)
        should_save_song = True
        # Check if file already exist, then ask user, if he wants to overwrite it:
        if os.path.isfile(path_to_file):
            screen_matrix = []
            line = []
            for i in range(64):
                line.append(' ')
            for i in range(17):
                screen_matrix.append(line[:])
            for i in range(len(path_to_file)):
                screen_matrix[0][i] = path_to_file[i]
            ok_selected = warning_window.main(keypad, screen_matrix, 'overwrite song')
            if ok_selected:
                os.remove(path_to_file)
            else:
                # User picked to not overwrite in warning window:
                should_save_song = False
    if should_save_song and path_to_file is not None:
        with open(path_to_file, 'wb') as file_btp:
            pickle.dump(song_data, file_btp)

def load_song(song_data, keypad):
    path_to_file = pick_file.get_filename('load song', keypad)
    if path_to_file is not None:
        with open(path_to_file, 'rb') as file_btp:
            song_data = pickle.load(file_btp)
        clear_temp()
        # Create temporary audio files adjusted for pygame mixer settings:
        samples = song_data.get_data('samples')
        samples_temp = song_data.get_data('samples_temp')
        for i in range(len(samples)):
            if samples[i] != 'Empty':
                samples_temp[i] = convert_audio_to_temp.convert_to_pygame_format(samples[i])
        convert_non_defaults(song_data)
        song_data.put_data('samples_temp', samples_temp)
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
def pots_values_tui(song_data, previous_printed_values, playlist_cursor, 
                    song_playlist, playlist_list_of_instruments,
):
    # Get potentiometers transformed data from data storage object:
    bpm = song_data.get_data('bpm')
    swing = song_data.get_data('swing')
    bvol = song_data.get_data('bvol')
    if previous_printed_values[0] != bpm or previous_printed_values[1] != swing or previous_printed_values[2] != bvol:
        clear_screen()
        tui_pl(tui_cursor = playlist_cursor[:], 
                    playlist = song_playlist, 
                    menu_selected = None, 
                    list_of_instruments = playlist_list_of_instruments, 
                    bpm = bpm, 
                    swing = swing, 
                    bvol = bvol,
                    songname = song_data.get_data('song_name'),
                    is_playing = song_data.get_data('is_playing')
                   )
        previous_printed_values[0] = bpm
        previous_printed_values[1] = swing    
        previous_printed_values[2] = bvol
    return previous_printed_values

def direction_keypad(key, playlist_cursor, song_playlist, playlist_list_of_instruments):
    # keypad 2 and 8 are up and down keypad, keypad 4 and 6 are left and right keypad
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
def edit_key(keypad, song_data, playlist_cursor, song_playlist):
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
            pattern_number_for_tracker = tracker.main(keypad, song_data, pattern_number_for_tracker)
        elif playlist_cursor[0] > 0 and playlist_list_of_instruments[playlist_cursor[0]] != 'Empty':
            pattern_number_for_tracker = pianoroll.main(keypad = keypad, 
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
                    song_data.last_added(target = 'playlist', 
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
                    song_data.last_added(target = 'playlist', 
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

def menu_accept_key(keypad, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments, selected, data_for_threads):
    # Store Queue and USB player for that software run instance.
    serial_usb = song_data.get_data('serial_usb')
    queue_player = song_data.get_data('queue_player')


    screen_matrix = tui_get_screen_matrix(tui_cursor=playlist_cursor[:], 
                                playlist=song_playlist, 
                                menu_selected=None, 
                                list_of_instruments=playlist_list_of_instruments, 
                                bpm=song_data.get_data('bpm'),
                                swing=song_data.get_data('swing'), 
                                bvol=song_data.get_data('bvol'),
                                songname=song_data.get_data('song_name'),
                                is_playing = song_data.get_data('is_playing')
                               )
    # Accept choice:
    if selected == 0:
        # Save song:
        song_data.put_data('serial_usb', None)
        song_data.put_data('queue_player', None)
        save_song(song_data, keypad)
        song_data.put_data('serial_usb', serial_usb)
        song_data.put_data('queue_player', queue_player)
        clear_screen()
        tui_pl(tui_cursor=playlist_cursor[:], 
                    playlist=song_playlist, 
                    menu_selected=selected, 
                    list_of_instruments=playlist_list_of_instruments, 
                    bpm=song_data.get_data('bpm'),
                    swing=song_data.get_data('swing'), 
                    bvol=song_data.get_data('bvol'),
                    songname=song_data.get_data('song_name'),
                    is_playing = song_data.get_data('is_playing')
                    )
    elif selected > 0:
        if selected == 1:
            warning_text = 'load song'
        if selected == 2:
            warning_text = 'new song'
        if selected == 3:
            warning_text = 'clear all tracks'

        ok_selected = warning_window.main(keypad, screen_matrix, warning_text)
        if ok_selected:
            if selected == 1 or selected == 2:
                # Send info to potetniometer thread, that is need to stop, beacuse new song_data is loaded
                song_data.put_data('is_playing', False)
                song_data.put_data('is_song_playing', False)
                if selected == 1:
                    # Load Song
                    temp_song_data = load_song(song_data, keypad)
                    if temp_song_data is not None:
                        song_data = temp_song_data
                elif selected == 2:
                    # new song: clear all previous data without serial_usb
                    song_data = SongData()
                    create_empty_song_playlist(song_data)
                    time.sleep(0.1) #to properly reload potentiometers on I2C
                    song_data.new_nondefaults() #Create new list of nondefaults notes
                # Put queue and serial to song data:
                song_data.put_data('serial_usb', serial_usb)
                song_data.put_data('queue_player', queue_player)
                # Update samples in player in another process:
                samples_temp = song_data.get_data('samples_temp')
                send_to_player = SendToPlayer(queue_player)
                send_to_player.update_all_samples(samples_temp)
                send_to_player.create_new_nondefault()
                # Update threads with reference to new song_data object:
                data_for_threads[0] = song_data
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
        else:
            # Action was not confirmed by user in warning window
            # display menu without warning:
            clear_screen()
            tui_pl(tui_cursor=playlist_cursor[:], 
                        playlist=song_playlist, 
                        menu_selected=selected, 
                        list_of_instruments=playlist_list_of_instruments, 
                        bpm=song_data.get_data('bpm'),
                        swing=song_data.get_data('swing'), 
                        bvol=song_data.get_data('bvol'),
                        songname=song_data.get_data('song_name'),
                        is_playing = song_data.get_data('is_playing')
                        )
    
# Enter menu to save or load song:
def menu(keypad, song_data, playlist_cursor, song_playlist, playlist_list_of_instruments, data_for_threads):    
    selected = 0
    menu_cursor = [0, 0]
    clear_screen()
    tui_pl(tui_cursor=playlist_cursor[:], 
                playlist=song_playlist, 
                menu_selected=selected, 
                list_of_instruments=playlist_list_of_instruments, 
                bpm=song_data.get_data('bpm'),
                swing=song_data.get_data('swing'), 
                bvol=song_data.get_data('bvol'),
                songname=song_data.get_data('song_name'),
                is_playing = song_data.get_data('is_playing')
               )    
    while True:
        key = keypad.check_keys()
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
                new_song_data = menu_accept_key(keypad, song_data, playlist_cursor, 
                                                song_playlist, playlist_list_of_instruments, 
                                                selected, data_for_threads
                                                )
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
                tui_pl(tui_cursor=playlist_cursor[:], 
                            playlist=song_playlist, 
                            menu_selected=selected, 
                            list_of_instruments=playlist_list_of_instruments, 
                            bpm=song_data.get_data('bpm'),
                            swing=song_data.get_data('swing'), 
                            bvol=song_data.get_data('bvol'),
                            songname=song_data.get_data('song_name'),
                            is_playing = song_data.get_data('is_playing')
                            )
                previous_selected = selected 

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
    
def main(keypad, song_data, data_for_threads):
    create_empty_song_playlist(song_data)
    previous_printed_values = [0, 0, 0]
    # Playlist loop:
    while True:
        # Get lists from data storage:
        playlist_cursor = song_data.get_data('playlist_cursor')
        song_playlist = song_data.get_data('song_playlist')
        playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
        
        # Update screen, if any value from potentiometers has changed:
        previous_printed_values = pots_values_tui(song_data, previous_printed_values, 
                                                  playlist_cursor, song_playlist, playlist_list_of_instruments
                                                  )
        # Get key from keypad:    
        key = keypad.check_keys()
        if key != '':
            # keypad 2 and 8 are up and down keypad, keypad 4 and 6 are left and right keypad
            if key == '2' or key == '4' or key == '6' or key == '8':
                playlist_cursor = direction_keypad(key, playlist_cursor, song_playlist, playlist_list_of_instruments)        
            # Key with [E] sticker on it - edit selected pattern:
            elif key == '3':
                create_empty_song_playlist(song_data)
                song_playlist = song_data.get_data('song_playlist')
                edit_key(keypad, song_data, playlist_cursor, song_playlist)
                playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
            # keypad with [+] and [-] sticker - changing selected values:    
            elif key == '7' or key == '9':
                result = plus_n_minus_keypad(key, playlist_cursor, song_data, song_playlist, playlist_list_of_instruments)
                if result is not None:
                    if result[0] == 'playlist':
                        playlist = result[1]
                    else:
                        playlist_list_of_instruments = result[1]
            # Key with [C] sticker - clear track on which cursor is present:
            elif key == '0':
                # get currently displayed GUI:
                screen_matrix = tui_get_screen_matrix(tui_cursor=playlist_cursor[:], 
                                                        playlist=song_playlist, 
                                                        menu_selected=None, 
                                                        list_of_instruments=playlist_list_of_instruments, 
                                                        bpm=song_data.get_data('bpm'),
                                                        swing=song_data.get_data('swing'), 
                                                        bvol=song_data.get_data('bvol'),
                                                        songname=song_data.get_data('song_name'),
                                                        is_playing = song_data.get_data('is_playing')
                                                       )
                song_playlist = clear_key(keypad, screen_matrix, song_playlist, playlist_cursor)
            # Key with [M] sticker - menu:
            elif key == '#':
                # Enter menu to save or load song or to clear entinre playlist:
                new_song_data = menu(keypad, song_data, playlist_cursor, 
                                     song_playlist, playlist_list_of_instruments, 
                                     data_for_threads
                                     )
                if new_song_data is not None:
                    song_data = new_song_data
                    song_playlist = song_data.get_data('song_playlist')
                    playlist_list_of_instruments = song_data.get_data('playlist_list_of_instruments')
                    playlist_cursor = [0, 0]
                    clear_screen()
                    tui_pl(tui_cursor=playlist_cursor[:], 
                                playlist=song_playlist, 
                                menu_selected = None,
                                list_of_instruments=playlist_list_of_instruments, 
                                bpm=song_data.get_data('bpm'),
                                swing=song_data.get_data('swing'), 
                                bvol=song_data.get_data('bvol'),
                                songname=song_data.get_data('song_name'),
                                is_playing = song_data.get_data('is_playing')
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
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = song_data.last_added('playlist', playlist_cursor[0])
                    # delete pattern:    
                    else:
                        song_playlist[playlist_cursor[0]][playlist_cursor[1] - 1] = ' '
            
            # when key was pressed, update displayed GUI:
            clear_screen()
            tui_pl(tui_cursor = playlist_cursor[:], 
                        playlist = song_playlist, 
                        menu_selected = None, 
                        list_of_instruments = playlist_list_of_instruments, 
                        bpm=song_data.get_data('bpm'),
                        swing=song_data.get_data('swing'), 
                        bvol=song_data.get_data('bvol'),
                        songname = song_data.get_data('song_name'),
                        is_playing = song_data.get_data('is_playing')
                       )    
        
        # Update values in data storage:
        song_data.put_data('playlist_cursor', playlist_cursor)
        song_data.put_data('song_playlist', song_playlist)
        song_data.put_data('playlist_list_of_instruments', playlist_list_of_instruments)

if __name__ == '__main__':
    playlist_loop()
