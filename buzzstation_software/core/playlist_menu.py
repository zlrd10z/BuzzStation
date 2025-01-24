import os
from tui import load_scrn
from tui import tui_warning_window
from tui import tui_playlist
from tui.tui_playlist_menu import display_menu_window
from .song_data import SongData
from . import pick_file
from core import warning_window
from copy import deepcopy
import pickle
from . import convert_audio_to_temp
from core.player_proc import SendToPlayer
import time


'''
When new song loaded (song_data), then update dictionary data_for_threads with new reference,
other threads, like player thread, which handle playing audio samples and sending MIDI signals,
checks in loop, if his reference it's up to date with one in data_for_thread.
'''
def update_samples_and_song(song_data, data_for_threads):
    # Update samples in player in another process:
    queue_player = data_for_threads['queue_player']
    samples_temp = song_data.get_data('samples_temp')
    send_to_player = SendToPlayer(queue_player)
    send_to_player.update_all_samples(samples_temp)
    send_to_player.create_new_nondefault()
    # Update threads with reference to new song_data object:
    data_for_threads['song_data'] = song_data

def create_empty_song_playlist(song_data):
    song_playlist = song_data.get_data('song_playlist')
    track_for_instrument = []
    for i in range(16):
        track_for_instrument.append(' ')
    song_playlist.append(track_for_instrument)
    song_data.put_data('song_playlist', song_playlist)

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
def new_song():
    song_data = SongData()
    create_empty_song_playlist(song_data)
    time.sleep(0.1) #to properly reload potentiometers on I2C
    song_data.new_nondefaults() #Create new list of nondefaults notes
    return song_data

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
            for i in range(len(screen_matrix[0])):
                if i < len(path_to_file):
                    screen_matrix[0][i] = path_to_file[i]
                else:
                    break
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

def clear_all_tracks(song_data):
    # Clear entire playlist:
    song_playlist = song_data.get_data('song_playlist')
    track_for_instrument = []
    for i in range(16):
        track_for_instrument.append(' ')
    for i in range(len(song_playlist)):
        song_playlist[i] = track_for_instrument[:]
    song_data.put_data('song_playlist', song_playlist)
    return song_data

def clear_selected(song_data, selection, playlist_cursor):
    playlist = song_data.get_data('song_playlist')
    sel_start_xy = selection.get('sel_start_xy')
    sel_end_xy = selection.get('sel_end_xy')
    if sel_start_xy is None or sel_end_xy is None:
        return None
    for i in range(sel_start_xy[0], sel_end_xy[0]+1):
        for j in range(sel_start_xy[1], sel_end_xy[1]+1):
            print(i, j)
            playlist[i][j] = ' '
    song_data.put_data('song_playlist', playlist)

def reverse_playlist_chngs(undo, song_data):
    playlist = song_data.get_data('song_playlist')
    prev_data = undo.get()
    if prev_data is not None:
        prev_data = deepcopy(prev_data)
        playlist = prev_data
        song_data.put_data('song_playlist', playlist)

def update_selection(selection, playlist_cursor):
    plc = playlist_cursor[:]
    if plc[1] > 0:
        plc[1] -= 1
        # Start selection:
        if selection.get('sel_start_xy') is None:
            selection.update('sel_start_xy', plc)
            print('1')
        # End selection:
        elif selection.get('sel_end_xy') is None:
            sel_start_xy = selection.get('sel_start_xy')
            sel_end_xy = plc
            new_sel_start_xy = sel_start_xy[:]
            new_sel_end_xy = sel_end_xy[:]
            for i in range(2):
                if sel_start_xy[i] > sel_end_xy[i]:
                    new_sel_end_xy[i] = sel_start_xy[i]
                    new_sel_start_xy[i] = sel_end_xy[i]
            selection.update('sel_start_xy', new_sel_start_xy)        
            selection.update('sel_end_xy', new_sel_end_xy)
        # New selection:
        elif (
                (selection.get('sel_start_xy') is not None)
                and (selection.get('sel_end_xy') is not None)
            ):
            selection.update('sel_start_xy', plc)
            selection.update('sel_end_xy', None)
            print('3')

def paste_button(selection, song_data, cursor):
    if selection.get('sel_end_xy') is None:
        return None
    # Copy selected pattern range, and paste it from playlist cursor postion
    playlist = song_data.get_data('song_playlist')
    sel_start_x, sel_start_y = selection.get('sel_start_xy')
    sel_end_x, sel_end_y = selection.get('sel_end_xy')
    i_range = sel_end_x - sel_start_x + 1
    j_range = sel_end_y - sel_start_y + 1
    #copypaste:
    for i in range(i_range):
        for j in range(j_range):
            # adjust playlist size if is less than needed:
            if (cursor[1]-1+j) > (len(playlist[i])-1):
                diff = (cursor[1]+j-1) - (len(playlist[i]) - 1)
                needed = int(diff / 16)
                if diff % 16 > 0:
                    needed += 16
                for m in range(len(playlist)):
                    for k in range(needed):
                        playlist[m].append(' ')
            playlist[cursor[0]+i][cursor[1]-1+j] = playlist[sel_start_x+i][sel_start_y+j]
    song_data.put_data('song_playlist', playlist)

def cursor_ops(selected_button, playlist_cursor, song_playlist):
    match selected_button:
        case '+16lvl':
            if (playlist_cursor[1]+16) <= (len(song_playlist[0])-1):
                playlist_cursor[1] += 16
        case '-16lvl':
            if (playlist_cursor[1]-16) >= 0:
                playlist_cursor[1] -= 16
        #first cursor lvl 0 is for instrumetnts bar
        case 'Begining':
            playlist_cursor[1] = 0
        #...so each playlist lvl is counterd from 1:
        case 'End':
            playlist_cursor[1] = len(song_playlist[0]) 
    return playlist_cursor

def menu_inputs(
                keypad, display_tui, song_data, playlist_cursor, 
                song_playlist, playlist_list_of_instruments, selection,
                screen_matrix
                ):
    button_titles = [
                     ['+16lvl', '-16lvl', 'Begining', 'End'],
                     ['Select', 'Unselect'],
                     ['CopyPaste', 'Undo', 'Clear Selected Patterns'],
                     ['Save Song', 'Load Song', 'New Song'],
                     ['Clear Enitre Playlist']
                    ]
    menu_cursor = [0, 0]
    selected_button = button_titles[menu_cursor[0]][menu_cursor[1]]
    display_menu_window(screen_matrix, selected_button, selection, playlist_list_of_instruments)

    while True:
        key = keypad.check_keys()
        if key != '':
            previous_menu_cursor = menu_cursor[:]
            # direction key - left:
            if key == '4':
                if menu_cursor[1] > 0:
                    menu_cursor[1] -= 1
            # direction key - right:
            elif key == '6':
                if menu_cursor[1] < (len(button_titles[menu_cursor[0]]) - 1):
                    menu_cursor[1] += 1
            # direction key - up:
            elif key == '2':
                if menu_cursor[0] > 0:
                    menu_cursor[0] -= 1
                    if menu_cursor[1] > (len(button_titles[menu_cursor[0]]) - 1):
                        menu_cursor[1] = (len(button_titles[menu_cursor[0]]) - 1)
            # direction key - down:
            elif key == '8':
                if menu_cursor[0] < (len(button_titles) - 1):
                    menu_cursor[0] += 1
                    if menu_cursor[1] > (len(button_titles[menu_cursor[0]]) - 1):
                        menu_cursor[1] = (len(button_titles[menu_cursor[0]]) - 1)
            # esc key or menu key:
            elif key == '1' or key == '#':
                return 'Exit'
            # accept key:
            elif key == '5':
                return selected_button
            selected_button = button_titles[menu_cursor[0]][menu_cursor[1]]

            # Check if selected button changed and display it to user:
            if previous_menu_cursor != menu_cursor:
                display_menu_window(screen_matrix, selected_button, selection, playlist_list_of_instruments)
                previous_menu_cursor = menu_cursor 

def menu(
         keypad, display_tui, song_data, playlist_cursor, 
         song_playlist, playlist_list_of_instruments, 
         data_for_threads, selection, undo
         ):
    while True:
        screen_matrix = display_tui(
                                    song_data=song_data, 
                                    list_of_instruments=playlist_list_of_instruments, 
                                    tui_cursor=playlist_cursor[:], 
                                    playlist=song_playlist,
                                    selection=selection,
                                    printtui=False
                                    )
        selected_button = menu_inputs(
                                      keypad, display_tui, song_data, playlist_cursor[:], 
                                      song_playlist, playlist_list_of_instruments, selection,
                                      screen_matrix
                                      )
        match selected_button:
            # Move playlist cursor:
            case '+16lvl' | '-16lvl' | 'Begining' | 'End':
                playlist_cursor = cursor_ops(selected_button, playlist_cursor, song_playlist)
                return 'playlist cursor', playlist_cursor
            # Opeerations with selection:
            case 'Select':
                update_selection(selection, playlist_cursor)
                return None
            case 'Unselect':
                selection.update('sel_start_xy', None)
                selection.update('sel_end_xy', None)
                return None
            case 'CopyPaste':
                undo.put(song_playlist)
                paste_button(selection, song_data, playlist_cursor)
                return 'playlist', song_data.get_data('song_playlist')
            case 'Undo':
                reverse_playlist_chngs(undo, song_data)
                return 'playlist', song_data.get_data('song_playlist')
            case 'Clear Selected Patterns':
                undo.put(song_playlist)
                clear_selected(song_data, selection, playlist_cursor[:])
                return 'playlist', song_data.get_data('song_playlist')
            # Song data operations:
            case 'Save Song':
                save_song(song_data, keypad)
                return None
            case 'Load Song':
                ok_selected = warning_window.main(keypad, screen_matrix, 'load song')
                if ok_selected:
                    song_data = load_song(song_data, keypad)
                    update_samples_and_song(song_data, data_for_threads)
                    return 'song_data', song_data
            case 'New Song':
                ok_selected = warning_window.main(keypad, screen_matrix, 'new song')
                if ok_selected:
                    song_data = new_song()
                    update_samples_and_song(song_data, data_for_threads)
                    return 'song_data', song_data
            # Clear playlist without assigned istruments modification:
            case 'Clear Enitre Playlist':
                ok_selected = warning_window.main(keypad, screen_matrix, 'clear all tracks')
                if ok_selected:
                    song_data = clear_all_tracks(song_data)
                    return 'song_data', song_data
            case 'Exit':
                return None

