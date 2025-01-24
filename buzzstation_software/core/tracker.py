from tui import tui_tracker
from tui import load_scrn
from core import warning_window
from libs.keypad import Keypad
from core.song_data import SongData
from core.pick_file import get_filename
from core import convert_audio_to_temp
import os
import copy
from core.player_proc import SendToPlayer
import subprocess


#lambdas:
clear_screen = lambda: os.system('clear')

# Converst single non C5 note for single track
def convert_nondefault(song_data, track, note):
    samples = song_data.get_data('samples')
    sample_path = samples[track]
    if sample_path != 'Empty':
        convert_audio_to_temp.convert_to_pygame_format(sample_path, note)

# Convert all non C5 notes for single track:
def convert_all_nondefaults_track(song_data, track):
    samples_not_c5 = song_data.get_data('samples_not_c5')
    notes_for_track = samples_not_c5[track]
    notes_for_track = [*notes_for_track]
    for note in notes_for_track:
        convert_nondefault(song_data, track, note)


def remove_sample_nondefault(song_data, samples_to_be_removed):
    if isinstance(samples_to_be_removed, list):
        samples = song_data.get_data('samples')
        for i in range(len(samples_to_be_removed)):
            if None not in samples_to_be_removed[i]:
                track = samples_to_be_removed[i][0]
                note = samples_to_be_removed[i][1]
                sample = samples[track].split("/")[-1]
                if sample != 'Empty':
                    cwd = os.getcwd()
                    command = "rm " + cwd + "/.temp/" + sample + '_' + note
                    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_new_empty_pattern():
    pattern = []
    for i in range(16):
        #Max 16 samples:
        pattern_for_single_sample = []
        for j in range(16):
            #16 quarter notes in pattern:
            pattern_for_single_sample.append([])
        pattern.append(pattern_for_single_sample)
    return pattern

def check_if_pattern_is_empty(pattern):
    isEmpty = True
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if len(pattern[i][j]) == 2:
                isEmpty = False
    return isEmpty

def menu(song_data, samples, pattern, pattern_number, song_name, 
         tracker_cursor, keys, tuitracker, tuitracker_noprinting
):
    def toggle_patterns(song_data, pattern_number, selected):
        new_pattern_number = pattern_number
        if pattern_number - 1 > 0 or pattern_number + 1 < 999:
            # update pattern in data storage:
            song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
            # Toggle down:
            if selected == 0:
                new_pattern_number = pattern_number - 1
            # Toggle up:
            elif selected == 1:
                new_pattern_number = pattern_number + 1
        return new_pattern_number
    
    def clone_pattern(song_data, pattern_number, selected, pattern):
        new_pattern_number = pattern_number
        for i in range(1, 998):
            if not song_data.drums_pattern_operations('exists', i):
                # Update pattern order list:
                new_pattern_number = i
                song_data.drums_pattern_operations('create or update pattern', new_pattern_number, copy.deepcopy(pattern))
                pattern = song_data.drums_pattern_operations('get pattern', new_pattern_number) 
                song_data.nondefault_note_counter(operation='increase', 
                                                 pattern=pattern
                                                 )
                break
        return new_pattern_number
    
    # Clear entire pattern:
    def clear_pattern(keys, screen_matrix, song_data, tuitracker, pattern_number):
        ok_selected = warning_window.main(keys, screen_matrix, 'clear all tracks')
        if ok_selected:
            pattern = song_data.drums_pattern_operations('get pattern', pattern_number) 
            samples_to_be_removed = song_data.nondefault_note_counter(operation='decrease', 
                                                                     pattern=pattern
                                                                     )
            
            remove_sample_nondefault(song_data, samples_to_be_removed)
            pattern = create_new_empty_pattern()
            song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
        
    
    menu_cursor = [0, 0]
    selected = 0

    
    tuitracker(samples_list=samples, 
               this_pattern=pattern, 
               pattern_number=pattern_number, 
               song_name=song_name, 
               selected_button=selected, 
               cursor=tracker_cursor
              )

    while True:
        key = keys.check_keys()
        if key != '':
            # Menu up
            if key == '2':
                if menu_cursor[0] > 0:
                    menu_cursor[0] -= 1
            #Menu down
            elif key == '8':
                if menu_cursor[0] < 2:
                    menu_cursor[0] += 1
            #menu left
            elif key == '4':
                if menu_cursor[1] == 1:
                    menu_cursor[1] = 0
            #menu right    
            elif key == '6':
                if menu_cursor[1] == 0:
                    menu_cursor[1] = 1        
            #escape button - exit menu, go back to playlist:
            elif key == '1' or key == '#':
                break
            # [insert] key - accept:
            elif key == '5':
                if selected < 3:
                    # toggling up/down patterns:
                    if selected < 2:
                        result = toggle_patterns(song_data, pattern_number, selected)
                    # clone pattern:
                    if selected == 2:
                        result = clone_pattern(song_data, pattern_number, selected, pattern)
                    return result
                #clear pattern:
                elif selected == 3:
                    screen_matrix = tuitracker_noprinting(samples_list=samples, 
                                                           this_pattern=pattern, 
                                                           pattern_number=pattern_number, 
                                                           song_name=song_name, 
                                                           selected_button=selected, 
                                                           cursor=tracker_cursor
                                                         )
                    clear_pattern(keys, screen_matrix, song_data, tuitracker, pattern_number)
                    break
                    
            # Update selected (selected is another value:
            if menu_cursor[0] == 0:
                selected = menu_cursor[1]
            elif menu_cursor[0] == 1:
                selected = 2
            elif menu_cursor[0] == 2:
                selected = 3

            # when key was pressed, display updated GUI:
            
            tuitracker(samples_list=samples, 
               this_pattern=pattern, 
               pattern_number=pattern_number, 
               song_name=song_name, 
               selected_button=selected, 
               cursor=tracker_cursor
               )    

def clear_single_track(song_data, keys, tracker_cursor, screen_matrix, pattern, pattern_number):
    ok_selected = warning_window.main(keys, screen_matrix, 'clear track')
    if ok_selected:
        for i in range(16):
            pattern[tracker_cursor[0]][i] = []
            song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
        return pattern
            
# This function check if any value from potentiometer, and if it's true, it's displaying new value on screen: 
def pots_values_tui(song_data, samples, pattern, pattern_number, 
                    song_name, tracker_cursor, potentiometers_previous_values,
                    tuitracker
):
    bpm = song_data.get_data('bpm')
    swing = song_data.get_data('swing')
    bvol = song_data.get_data('bvol')
    if bpm != potentiometers_previous_values[0] or swing != potentiometers_previous_values[1] or bvol != potentiometers_previous_values[2]:
        potentiometers_previous_values[0] = bpm
        potentiometers_previous_values[1] = swing
        potentiometers_previous_values[2] = bvol
        
        tuitracker(samples_list=samples, 
                   this_pattern=pattern, 
                   pattern_number=pattern_number, 
                   song_name=song_name, 
                   selected_button=None, 
                   cursor=tracker_cursor
                  )
    return potentiometers_previous_values

def direction_keys(dir_key, tracker_cursor, pattern):
    def up(tracker_cursor):
        if tracker_cursor[1] - 1 >= 0:
            tracker_cursor[1] -= 1
        else: tracker_cursor[1] = 16
        return tracker_cursor
    
    def down(tracker_cursor):
        if tracker_cursor[1] + 1 <= 16:
            tracker_cursor[1] += 1
        else: tracker_cursor[1] = 0
        return tracker_cursor

    def right(tracker_cursor, pattern):
        # move to next sample
        if tracker_cursor[1] == 0:
            if tracker_cursor[0] + 1 < 16:
                tracker_cursor[0] += 1
            else:
                tracker_cursor[0] = 0
        else:
            # move jump to next note, if current field is empty, ommit volume subfield:
            if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
                tracker_cursor[2] = 0
                if tracker_cursor[0] + 1 < 16:
                    tracker_cursor[0] += 1
                else:
                    tracker_cursor[0] = 0
            else:
                if tracker_cursor[2] == 1:
                    tracker_cursor[2] = 0
                    if tracker_cursor[0] + 1 < 16:
                        tracker_cursor[0] += 1
                    else:
                        tracker_cursor[0] = 0
                elif tracker_cursor[2] == 0:
                    tracker_cursor[2] = 1
        return tracker_cursor
                    
    def left(tracker_cursor, pattern):
        # move to previous sample
        if tracker_cursor[1] == 0:
            if tracker_cursor[0] - 1 >= 0:
                tracker_cursor[0] -= 1
            else:
                tracker_cursor[0] = 15
        else:
            # move jump to next note, if current field is empty, ommit volume subfield:
            if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
                tracker_cursor[2] = 1
                if tracker_cursor[0] - 1 > -1:
                    tracker_cursor[0] -= 1
                else:
                    tracker_cursor[0] = 15
            else:
                if tracker_cursor[2] == 0:
                    tracker_cursor[2] = 1
                    if tracker_cursor[0] - 1 > -1:
                        tracker_cursor[0] -= 1
                    else:
                        tracker_cursor[0] = 15
                elif tracker_cursor[2] == 1:
                    tracker_cursor[2] = 0    
        return tracker_cursor
    
    result = tracker_cursor
    match dir_key:
        case '2':
            result = up(tracker_cursor)
        case '8':
            result = down(tracker_cursor)
        case '4':
            result = left(tracker_cursor, pattern)
        case '6':
            result = right(tracker_cursor, pattern)
    return result

def change_note(operation, note_and_octave, tracker_cursor):
    notes_string_list = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_and_octave = note_and_octave.replace(' ', '')
    
    if operation == 'semitone down':
        octave = note_and_octave[-1:]
        note = note_and_octave[:-1]
        note_index = notes_string_list.index(note)
        # if sound is eg C5 then switch to note B4, octave cannot be lower than 1:
        if note_index == 0 and int(octave) >= 2: 
            note = notes_string_list[len(notes_string_list) - 1]
            octave = str( int(octave) - 1 )
        # If note is eg C#5, then switch note to C5    
        else: 
            note_index -= 1
            note = notes_string_list[note_index]    
        new_note = note + str(octave)        
    elif operation == 'semitone up':    
            # Change note value up:
        if tracker_cursor[2] == 0:
            octave = note_and_octave[-1:]
            note = note_and_octave[:-1]
            note_index = notes_string_list.index(note)
            # if sound is eg B5 then switch to note C6, octave cannot be higher than 7:
            if note_index == len(notes_string_list) - 1 and int(octave) <= 7: 
                note = notes_string_list[0]
                octave = str( int(octave) + 1 )
            # If note is eg C#5, then switch note to C5    
            else: 
                note_index += 1
                note = notes_string_list[note_index]
            new_note = note + str(octave)
    return new_note

# key with [+] sticker / key with [-] sticker: 
def plus_n_minus_keys(key, song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player):
    def minus_key(song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player):
        # if field on playlist is highlighted:
        if tracker_cursor[1] > 0:
            # Add note with volume:
            if len(pattern[tracker_cursor[0]][tracker_cursor[1]-1]) == 0:
                pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ['C5', 'F']
            else:
                # Change note value down:
                if tracker_cursor[2] == 0:
                    note_and_octave = pattern[tracker_cursor[0]][tracker_cursor[1]-1][tracker_cursor[2]]
                    samples_to_be_removed = song_data.nondefault_note_counter(operation='decrease', 
                                                                             track=tracker_cursor[0], 
                                                                             note=note_and_octave
                                                                             )
                    
                    remove_sample_nondefault(song_data, samples_to_be_removed)
                    new_note = change_note('semitone down', note_and_octave, tracker_cursor[:])
                    pattern[tracker_cursor[0]][tracker_cursor[1]-1][tracker_cursor[2]] = new_note
                    should_convert_sample = song_data.nondefault_note_counter(operation='increase', 
                                                                             track=tracker_cursor[0], 
                                                                             note=new_note
                                                                             )

                    if should_convert_sample:
                        convert_nondefault(song_data, tracker_cursor[0], new_note)
                        send_to_player.update_nondefault()

                # Change note's volume value:
                if tracker_cursor[2] == 1:
                    volume = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
                    volume_index = volume_string_list.index(volume)
                    if volume_index > 0:
                        volume_index -= 1
                        volume = volume_string_list[volume_index]
                    pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = volume
            note = [
                    pattern[tracker_cursor[0]][tracker_cursor[1]-1][0], 
                    pattern[tracker_cursor[0]][tracker_cursor[1] - 1][1]
                    ]
            song_data.last_added('tracker', tracker_cursor[0], note)

            # update pattern in data storage:
            song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
            return pattern
        else:
            # if sample highlighed on the screen, change volume of the sample:
            volumes = song_data.get_data('samples_volume')
            if volumes[tracker_cursor[0]] - 1 >= 0:
                volumes[tracker_cursor[0]] -= 1
                song_data.put_data('samples_volume', volumes)
    
    def plus_key(song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player):
        # if field on playlist is highlighted:
        if tracker_cursor[1] > 0:
            # Add note with volume:
            if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
                pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = ['C5', 'F']
            else:
                # semitone up:
                if tracker_cursor[2] == 0:
                    note_and_octave = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
                    samples_to_be_removed = song_data.nondefault_note_counter(operation='decrease', 
                                                                             track=tracker_cursor[0], 
                                                                             note=note_and_octave
                                                                             )
                    remove_sample_nondefault(song_data, samples_to_be_removed)
                    new_note = change_note('semitone up', note_and_octave, tracker_cursor[:])
                    pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = new_note
                    should_convert_sample = song_data.nondefault_note_counter(operation='increase', 
                                                                             track=tracker_cursor[0], 
                                                                             note=new_note
                                                                             )
                    if should_convert_sample:
                        convert_nondefault(song_data, tracker_cursor[0], new_note)
                        send_to_player.update_nondefault()

                # Change note's volume value:
                elif tracker_cursor[2] == 1:
                    volume = pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]]
                    volume_index = volume_string_list.index(volume)
                    if volume_index < len(volume_string_list) - 1:
                        volume_index += 1
                        volume = volume_string_list[volume_index]
                    pattern[tracker_cursor[0]][tracker_cursor[1] - 1][tracker_cursor[2]] = volume

            note = [pattern[tracker_cursor[0]][tracker_cursor[1] - 1][0], 
                    pattern[tracker_cursor[0]][tracker_cursor[1] - 1][1]
                    ]
            song_data.last_added('tracker', tracker_cursor[0], note)
            # update pattern in data storage:
            song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
            return pattern
        else:
            # if sample highlighed on the screen, change volume of the sample:
            volumes = song_data.get_data('samples_volume')
            if volumes[tracker_cursor[0]] + 1 <= 10:
                volumes[tracker_cursor[0]] += 1
                song_data.put_data('samples_volume', volumes)
    
    if key == '7':
        result = minus_key(song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player)
    if key == '9':
        result = plus_key(song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player)
    return result

# key with [insert] sticker on it - accept / insert key:
def insert_key(song_data, send_to_player, tracker_cursor, keys, pattern, pattern_number):
    # If cursor is on samples level, insert sample / change sample to other one:
    if tracker_cursor[1] == 0:
        # Choose sample from disk with get_filename function and get path to choosen sample:
        sample_path = get_filename('sample', keys)
        if sample_path is not None:
            samples = song_data.get_data('samples')
            # put path to samples list:
            samples[tracker_cursor[0]] = sample_path
            song_data.put_data('samples', samples)
            # generate temp sample file adjusted for pygame mixer settings:
            samples_temp = song_data.get_data('samples_temp')
            temp_sample_name = convert_audio_to_temp.convert_to_pygame_format(sample_path)
            samples_temp[tracker_cursor[0]] = temp_sample_name
            song_data.put_data('samples_temp', samples_temp)
            # send info to audio player, which sample changed and it's name:
            send_to_player.update_sample(tracker_cursor[0], temp_sample_name)
            convert_all_nondefaults_track(song_data, tracker_cursor[0])
            send_to_player.update_nondefault()

    # if cursor is on playlist:
    elif tracker_cursor[1] > 0:
        # if note is empty, add last added note:
        if len(pattern[tracker_cursor[0]][tracker_cursor[1] - 1]) == 0:
            last_added_note_data = song_data.last_added('tracker', tracker_cursor[0])[:]
            pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = last_added_note_data
            note = last_added_note_data[0]
            if ' ' in note:
                note = note.replace(' ', '')
            elif note != 'C5':
                should_convert_sample = song_data.nondefault_note_counter(operation='increase', 
                                                         track=tracker_cursor[0], 
                                                         note=note
                                                         )
                if should_convert_sample:
                    convert_nondefault(song_data, tracker_cursor[0], note)
                    send_to_player.update_nondefault()

        # if field for note is not empty, delete note:
        else:
            note = pattern[tracker_cursor[0]][tracker_cursor[1] - 1]
            note = note[0]
            pattern[tracker_cursor[0]][tracker_cursor[1] - 1] = []
            if note != 'C5':
                samples_to_be_removed = song_data.nondefault_note_counter(operation='decrease', 
                                                             track=tracker_cursor[0], 
                                                             note=note
                                                             )
                remove_sample_nondefault(song_data, samples_to_be_removed)


        # update pattern in data storage:
        song_data.drums_pattern_operations('create or update pattern', pattern_number, new_pattern=pattern)
        return pattern
    
def main(keys, song_data, pattern_number, data_for_threads):
    tuitracker = lambda samples_list, this_pattern, pattern_number, song_name, selected_button, cursor: tui_tracker.main(list_of_samples=samples_list, 
                                pattern=this_pattern, 
                                is_playing=song_data.get_data('is_playing'), 
                                bpm_value=song_data.get_data('bpm'), 
                                swing_value=song_data.get_data('swing'), 
                                vol_value=song_data.get_data('bvol'), 
                                pattern_number=pattern_number,
                                song_name=song_name,
                                selected_button=selected_button, 
                                cursor=cursor,
                                playing_mode=song_data.get_data('is_song_playing')
    )

    tuitracker_noprinting = lambda samples_list, this_pattern, pattern_number, song_name, selected_button, cursor: tui_tracker.main(list_of_samples=samples_list, 
                                    pattern=this_pattern, 
                                    is_playing=song_data.get_data('is_playing'), 
                                    bpm_value=song_data.get_data('bpm'), 
                                    swing_value=song_data.get_data('swing'), 
                                    vol_value=song_data.get_data('bvol'), 
                                    pattern_number=pattern_number,
                                    song_name=song_name,
                                    selected_button=selected_button, 
                                    cursor=cursor,
                                    print_on_screen=False,
                                    playing_mode=song_data.get_data('is_song_playing')
    )
    
    song_name = song_data.get_data('song_name')
    # put data requried to playing pattern in pattern play mode:
    song_data.put_data('playing_pattern', pattern_number)
    song_data.put_data('playing_track', 0)

    volume_string_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    tracker_cursor = [0, 0, 0]
    
    potentiometers_previous_values = [None, None, None]
    
    # If pattern does not exist already, then create new empty pattern:
    if not song_data.drums_pattern_operations('exists', pattern_number):
        song_data.drums_pattern_operations('create or update pattern', pattern_number, create_new_empty_pattern())
    
    # Load samples and pattern:
    samples = song_data.get_data('samples')
    pattern = song_data.drums_pattern_operations('get pattern', pattern_number)

    # communication with player audio process:
    queue_player = data_for_threads['queue_player']
    send_to_player = SendToPlayer(queue_player)

    while True:
        #Check if any value from potentiometers, and if it's true, it's displaying new value on screen: 
        temp_pot_values =  pots_values_tui(song_data, samples, pattern, pattern_number, 
                                           song_name, tracker_cursor, potentiometers_previous_values,
                                           tuitracker
                                          )
        if temp_pot_values is not None:
            potentiometers_previous_values = temp_pot_values

        # Get key from keypad
        key = keys.check_keys()
        if key != '':
            # Escape key:
            if key == '1':
                song_data.put_data('is_playing', False)
                song_data.put_data('instrument_played', None)
                pattern_is_empty = check_if_pattern_is_empty(pattern)
                if pattern_is_empty:
                        # Delete pattern from patterns list and pattern orders list:
                        song_data.drums_pattern_operations('delete_pattern', pattern_number)
                # exit to playlist:
                break
            elif key == '*':
                is_playing = song_data.get_data('is_playing')
                if is_playing:
                    song_data.put_data('is_playing', False)
                    song_data.put_data('instrument_played', None)
                else:
                    song_data.put_data('instrument_played', 0)
                    song_data.put_data('is_playing', True)
            # Direction keys:
            elif key == '8' or key == '2' or key == '4' or key == '6':
                tracker_cursor = direction_keys(key, tracker_cursor, pattern)
            # [+] and [-] keys:
            elif key == '7' or key == '9':
                # change selected note's volume value / change selected sample master volume value / change note to higher/lower note:
                new_pattern = plus_n_minus_keys(key, song_data, tracker_cursor, pattern, volume_string_list, pattern_number, send_to_player)
                if new_pattern is not None:
                    pattern = new_pattern
            # [Insert] key:
            elif key == '5':
                temp_pattern = insert_key(song_data, send_to_player, tracker_cursor, keys, pattern, pattern_number)
                if temp_pattern is not None:
                    pattern = temp_pattern
                samples = song_data.get_data('samples')
            #[C] key - clear single track:
            elif key == '0':
                screen_matrix = tuitracker(samples_list=samples, 
                           this_pattern=pattern, 
                           pattern_number=pattern_number, 
                           song_name=song_name, 
                           selected_button=None, 
                           cursor=tracker_cursor
                          )
                modified_pattern = clear_single_track(song_data, keys, tracker_cursor, screen_matrix, pattern, pattern_number)
                if modified_pattern is not None:
                    pattern = modified_pattern
            #[E] key -  Change playing mode from looping pattern to playing whole song:
            elif key == '3':
                is_song_playing = song_data.get_data('is_song_playing')
                if is_song_playing:
                    is_song_playing = False
                else:
                    is_song_playing = True
                song_data.put_data('is_song_playing', is_song_playing)    
            # Pattern Menu:
            elif key == '#':
                new_pattern_number = menu(song_data, samples, pattern, pattern_number, 
                                          song_name, tracker_cursor, keys, tuitracker,
                                          tuitracker_noprinting
                                         )
                pattern = song_data.drums_pattern_operations('get pattern', pattern_number)
                if new_pattern_number is not None:
                    return new_pattern_number
            # if key was pressed, update displayed tui:
            
            tuitracker(samples_list=samples, 
                       this_pattern=pattern, 
                       pattern_number=pattern_number, 
                       song_name=song_name, 
                       selected_button=None, 
                       cursor=tracker_cursor[:]
                      )
                    
if __name__ == '__main__':
    # Tests
    keys = Keypad()
    song_data = SongData()
    main(keys, song_data, 1)
