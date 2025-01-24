from core import warning_window
from tui import tui_pianoroll
from libs.keypad import Keypad
from .song_data import SongData
import copy
import os

clear_screen = lambda: os.system('clear')

def create_empty_pattern():
    pattern = []
    for i in range(16):
        l = []
        pattern.append(l)
    return pattern

def delete_from_pattern(pattern, beat, note):
    if len(pattern[beat]) > 0:
        for i in range(len(pattern[beat]) - 1, -1, -1):
            if pattern[beat][i] == note:
                pattern[beat].pop(i)
                break

def tui(song_data, pattern_number, midi_and_channel, 
        selected_note, selected_beat, pattern, selected_menu_button
):
    tui_pianoroll.main(
                      bpm_value=song_data.get_data('bpm'), 
                      swing_value=song_data.get_data('swing'), 
                      pattern_number=pattern_number, 
                      playing_mode=song_data.get_data('is_song_playing'), 
                      playing=song_data.get_data('is_playing'), 
                      midi_output_and_channel=midi_and_channel, 
                      selected_note=selected_note, 
                      selecteded_beat=selected_beat, 
                      pattern=pattern, 
                      selected_menu_button=selected_menu_button,
                      print_it=True
                     )            
    
def get_screen_matrix(song_data, pattern_number, midi_and_channel, 
                      selected_note, selected_beat, pattern, selected_menu_button
):
    screen_matrix = tui_pianoroll.main(bpm_value=song_data.get_data('bpm'), 
                                       swing_value=song_data.get_data('swing'), 
                                       pattern_number=pattern_number, 
                                       playing_mode=song_data.get_data('is_song_playing'), 
                                       playing=song_data.get_data('is_playing'), 
                                       midi_output_and_channel=midi_and_channel, 
                                       selected_note=selected_note, 
                                       selecteded_beat=selected_beat, 
                                       pattern=pattern, 
                                       selected_menu_button=selected_menu_button,
                                       print_it=False
                                      )
    return screen_matrix

def tui_edit_note_length(song_data, pattern_number, midi_and_channel, 
                         selected_note, selected_beat, pattern, selected_menu_button
):
    tui_pianoroll.main(
                      bpm_value=song_data.get_data('bpm'), 
                      swing_value=song_data.get_data('swing'), 
                      pattern_number=pattern_number, 
                      playing_mode=song_data.get_data('is_song_playing'), 
                      playing=song_data.get_data('is_playing'), 
                      midi_output_and_channel=midi_and_channel, 
                      selected_note=selected_note, 
                      selecteded_beat=selected_beat, 
                      pattern=pattern, 
                      selected_menu_button=selected_menu_button,
                      print_it=True,
                      note_length_edit=True
                    )
    
    
def menu(keypad, song_data, pattern_number, midi_and_channel, 
        selected_note_and_octave, selected_beat, pattern, pattern_notes_to_turn_off,
        track
):
    menu_selected_button = 0
    
    tui(song_data, pattern_number, midi_and_channel, 
        selected_note_and_octave, selected_beat, pattern[:], 
        selected_menu_button=menu_selected_button
       )
    while True:
        key = keypad.check_keys()
        if key != '':
            if key == '1' or key == '#':
                break
            # direction key - rigth:
            if key == '6':
                if menu_selected_button < 3:
                    menu_selected_button += 1
            # direction key - left:
            if key == '4':
                if menu_selected_button > 0:
                    menu_selected_button -= 1
            # accept key:
            if key == '5':
                if menu_selected_button != 1:
                    # previous pattern:
                    if menu_selected_button == 0:
                        pattern_number -= 1
                    # next pattern:
                    elif menu_selected_button == 3:
                        pattern_number += 1
                    # clone pattern:
                    elif menu_selected_button == 2:
                        cloned_pattern_number = None
                        for i in range(1, 1000):
                            if not song_data.pianoroll_pattern_operations(operation = 'exists', track = track, pattern_number = i):
                                cloned_pattern_number = i
                                break                                
                        if cloned_pattern_number is not None:
                            song_data.pianoroll_pattern_operations(operation = 'create or update pattern', 
                                          track = track, 
                                          pattern_number = cloned_pattern_number, 
                                          new_pattern = copy.deepcopy(pattern)
                                         )
                            song_data.pianoroll_pattern_operations(operation = 'create or update pattern', 
                                                                      track = track, 
                                                                      pattern_number = cloned_pattern_number, 
                                                                      new_pattern =  copy.deepcopy(pattern_notes_to_turn_off),
                                                                      target_notes_to_turn_off = True
                                                                     )
                            pattern_number = cloned_pattern_number
                    return pattern_number
                if menu_selected_button == 1:
                    is_song_playing = song_data.get_data('is_song_playing')

                    if is_song_playing: is_song_playing = False
                    else: is_song_playing = True

                    song_data.put_data('is_song_playing', is_song_playing)
                    
                    tui(song_data, pattern_number, midi_and_channel, 
                        selected_note_and_octave, selected_beat, pattern[:], 
                        selected_menu_button = menu_selected_button
                       )
            
            tui(song_data, pattern_number, midi_and_channel, 
                selected_note_and_octave, selected_beat, pattern[:], 
                selected_menu_button = menu_selected_button)
            

# This function check if any value from potentiometer, and if it's true, it's displaying new value on screen: 
def pots_values_tui(song_data, pattern_number, midi_and_channel, 
                    selected_note_and_octave, selected_beat, pattern,
                    previous_values
):
            if song_data.get_data('bpm') != previous_values[0] or song_data.get_data('swing') != previous_values[1]:
                previous_values[0] = song_data.get_data('bpm') 
                previous_values[1] = song_data.get_data('swing')
                
                tui(song_data, pattern_number, midi_and_channel, 
                    selected_note_and_octave, selected_beat, pattern[:], 
                    selected_menu_button = None
                   )
            return previous_values

def direction_keys(key, selected_beat, selected_note_and_octave, notes):
    # Direction key - left:
    if key == '4':
        if selected_beat > 0:
            selected_beat -= 1
        else:
            selected_beat = 15
    # Direction key - right:
    if key == '6':
        if selected_beat < 15:
            selected_beat += 1
        else:
            selected_beat = 0
    # Direction key - up:
    if key == '2':
        note = selected_note_and_octave[:-1]
        octave = selected_note_and_octave[-1]
        index = notes.index(note)
        if index + 1 < len(notes):
            note = notes[index + 1]
        else:
            if int(octave) < 8:
                note = notes[0]
                octave = int(octave) + 1
        selected_note_and_octave = note + str(octave)
    # Direction key - down:
    if key == '8':
        note = selected_note_and_octave[:-1]
        octave = selected_note_and_octave[-1]
        index = notes.index(note)
        if index > 0:
            note = notes[index - 1]
        else:
            if int(octave) > 1:
                note = notes[-1]
                octave = int(octave) - 1
        selected_note_and_octave = note + str(octave)
    return(selected_beat, selected_note_and_octave)

# insert/accept key:
def insert_key(song_data, pattern, pattern_notes_to_turn_off, 
               selected_beat, selected_note_and_octave, track,
               pattern_number
):
    already_exists = False
    index = None
    #check if note not exist already on selected beat:
    if len(pattern[selected_beat]) > 0:
        for i in range(len(pattern[selected_beat])):
            if pattern[selected_beat][i][0] == selected_note_and_octave:
                already_exists = True
                index = i
                break
    if not already_exists:
        pattern[selected_beat].append([selected_note_and_octave, 1, 8])
        pattern_notes_to_turn_off[selected_beat].append(selected_note_and_octave)
    elif already_exists:
        pattern[selected_beat].pop(index)
        # search for end of the note and delete it:
        for i in range(len(pattern_notes_to_turn_off[selected_beat])):
            if pattern_notes_to_turn_off[selected_beat][i] == selected_note_and_octave:
                pattern_notes_to_turn_off[selected_beat].pop(i)
                break
    # Update pattern with start of notes and with end of notes in data storage:
    song_data.pianoroll_pattern_operations(operation='update pattern', 
                                          track=track, 
                                          pattern_number=pattern_number, 
                                          new_pattern=pattern
                                          )

    song_data.pianoroll_pattern_operations(operation='update pattern', 
                                          track=track, 
                                          pattern_number=pattern_number, 
                                          new_pattern=pattern_notes_to_turn_off, 
                                          target_notes_to_turn_off=True
                                          )
    return song_data

def edit_key(keypad, song_data, pattern_number, 
             midi_and_channel, selected_beat,
             track, selected_note_and_octave
):
    pattern = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                     track=track, 
                                                     pattern_number=pattern_number
                                                    )

    pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                       track=track,
                                                                       pattern_number=pattern_number,
                                                                       target_notes_to_turn_off=True
                                                                      )
    if len(pattern[selected_beat]) > 0:
        for i in range(len(pattern[selected_beat])):
            if selected_note_and_octave == pattern[selected_beat][i][0]:
                
                tui_edit_note_length(song_data, pattern_number, midi_and_channel, 
                                     selected_note_and_octave, selected_beat, pattern[:], 
                                     selected_menu_button=None
                                    )
                while True:
                    key = keypad.check_keys()
                    if key != '':
                        if key == '1' or key == '3' or key == '5': 
                            return song_data
                        # Shorten the note by a quarter note:
                        elif key == '7' or key == '4':
                            if pattern[selected_beat][i][1] > 1:
                                delete_from_pattern(pattern_notes_to_turn_off, pattern[selected_beat][i][1] - 1 + selected_beat, pattern[selected_beat][i][0])
                                pattern[selected_beat][i][1] -= 1
                                pattern_notes_to_turn_off[pattern[selected_beat][i][1] - 1 + selected_beat].append(pattern[selected_beat][i][0])
                        # lengthen the note by a quarter note:
                        elif key == '9' or key == '6': 
                            if 16 - selected_beat > pattern[selected_beat][i][1]:
                                # check if there is no note behind this note:
                                if len(pattern[selected_beat + pattern[selected_beat][i][1]]) > 0:
                                    same_note_exists_one_quarter_behind = False
                                    for j in range(len(pattern[selected_beat + pattern[selected_beat][i][1]])):
                                        if pattern[selected_beat + pattern[selected_beat][i][1]][j][0] == selected_note_and_octave:
                                            same_note_exists_one_quarter_behind = True
                                            break
                                    if same_note_exists_one_quarter_behind == False:
                                        # Remove previous note's length and update with new one:
                                        delete_from_pattern(pattern_notes_to_turn_off, pattern[selected_beat][i][1] - 1 + selected_beat, pattern[selected_beat][i][0])
                                        pattern[selected_beat][i][1] += 1
                                        pattern_notes_to_turn_off[pattern[selected_beat][i][1] - 1 + selected_beat].append(pattern[selected_beat][i][0])
                                else:
                                    delete_from_pattern(pattern_notes_to_turn_off, pattern[selected_beat][i][1] - 1 + selected_beat, pattern[selected_beat][i][0])
                                    pattern[selected_beat][i][1] += 1
                                    pattern_notes_to_turn_off[pattern[selected_beat][i][1] - 1 + selected_beat].append(pattern[selected_beat][i][0])
                        # Update pattern with start of notes and with end of notes in data storage:
                        song_data.pianoroll_pattern_operations(operation='update pattern', 
                                                               track=track, 
                                                               pattern_number=pattern_number, 
                                                               new_pattern=pattern
                                                              )
                        song_data.pianoroll_pattern_operations(operation='update pattern', 
                                                               track=track, 
                                                               pattern_number=pattern_number, 
                                                               new_pattern=pattern_notes_to_turn_off, 
                                                               target_notes_to_turn_off=True
                                                              )
                        
                        tui_edit_note_length(song_data, pattern_number, midi_and_channel, 
                                             selected_note_and_octave, selected_beat, pattern[:], 
                                             selected_menu_button=None
                                            )

# This function clear all notes, but leaves rest of the settings:
def clear_key(song_data, pattern_number, midi_and_channel, 
              selected_note_and_octave, selected_beat,
              track, screen_matrix, keypad
):
    song_data.put_data('is_playing', False)
    ok_selected = warning_window.main(keypad, screen_matrix, 'clear pattern')
    if ok_selected:
        # Clear pattern:
        pattern = create_empty_pattern()
        pattern_notes_to_turn_off = create_empty_pattern()
        # Update pattern with start of notes and with end of notes in data storage:
        song_data.pianoroll_pattern_operations(operation='create or update pattern', 
                                                  track=track, 
                                                  pattern_number=pattern_number, 
                                                  new_pattern=pattern
                                                 )
        song_data.pianoroll_pattern_operations(operation='create or update pattern', 
                                                  track=track, 
                                                  pattern_number=pattern_number, 
                                                  new_pattern=pattern_notes_to_turn_off, 
                                                  target_notes_to_turn_off=True
                                                 )

def volume_up_down_keys(key, song_data, pattern, pattern_number, selected_beat, selected_note_and_octave, track):
    if key == '9':
        if len(pattern[selected_beat]) > 0:
            for i in range(len(pattern[selected_beat])):
                if pattern[selected_beat][i][0] == selected_note_and_octave:
                    if pattern[selected_beat][i][2] < 8:
                        pattern[selected_beat][i][2] += 1
                        song_data.pianoroll_pattern_operations('update pattern', track, pattern_number, pattern[:])
    # volume down note:
    if key == '7':
        if len(pattern[selected_beat]) > 0:
            for i in range(len(pattern[selected_beat])):
                if pattern[selected_beat][i][0] == selected_note_and_octave:
                    if pattern[selected_beat][i][2] > 1:
                        pattern[selected_beat][i][2] -= 1
                        song_data.pianoroll_pattern_operations('update pattern', track, pattern_number, pattern[:])
    return song_data
      
def main(keypad, song_data, pattern_number, midi_and_channel, track):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    selected_note_and_octave = 'C5'
    selected_beat = 0
    
    # Check is this pattern exist or this is new pattern:
    if song_data.pianoroll_pattern_operations(operation = 'exists', track = track, pattern_number = pattern_number):
        pattern = song_data.pianoroll_pattern_operations(operation = 'get pattern for single track', 
                                                         track = track, 
                                                         pattern_number = pattern_number
                                                        )
        
        pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get pattern for single track', 
                                                                           track = track,
                                                                           pattern_number = pattern_number,
                                                                           target_notes_to_turn_off = True
                                                                          )
    else:
        #create new pattern:
        pattern = create_empty_pattern()
        pattern_notes_to_turn_off = create_empty_pattern()
        song_data.pianoroll_pattern_operations(operation = 'create or update pattern', 
                                               track = track, 
                                               pattern_number = pattern_number, 
                                               new_pattern = pattern[:]
                                              )
        song_data.pianoroll_pattern_operations(operation = 'create or update pattern', 
                                               track = track, 
                                               pattern_number = pattern_number, 
                                               new_pattern = pattern_notes_to_turn_off[:], 
                                               target_notes_to_turn_off = True
                                              )
    previous_values = [None, None]
    # put data requried to playing pattern in pattern play mode:
    song_data.put_data('playing_pattern', pattern_number)
    song_data.put_data('playing_track', track+1)
    
    # main loop:
    while True:
        #check if values from potentiometers changed, and if yes, update values on GUI:
        previous_values = pots_values_tui(song_data, pattern_number, midi_and_channel, 
                                          selected_note_and_octave, selected_beat, pattern,
                                          previous_values
                                         )
        
        key = keypad.check_keys()
        if key != '':
            # Direction keys:
            if key == '4' or key == '8' or key == '6' or key == '2':
                selected_beat, selected_note_and_octave = direction_keys(key, selected_beat, 
                                                                         selected_note_and_octave, 
                                                                         notes
                                                                        )
            # Escape key:
            if key == '1':
                song_data.put_data('is_playing', False)
                song_data.put_data('is_song_playing', False)
                song_data.put_data('instrument_played', None)
                key = ''
                break
            # play/pause key:
            if key == '*':
                is_playing = song_data.get_data('is_playing')
                pattern_exist = song_data.pianoroll_pattern_operations('exists', track, pattern_number)
                if is_playing:
                    song_data.put_data('is_playing', False)
                    song_data.put_data('instrument_played', None)
                elif not is_playing and pattern_exist:
                    song_data.put_data('instrument_played', track)
                    song_data.put_data('is_playing', True)
            # Insert / accept key:
            if key == '5':
                song_data = insert_key(song_data, pattern, pattern_notes_to_turn_off, selected_beat, 
                                      selected_note_and_octave, track, pattern_number
                                      )
                pattern = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                 track=track, 
                                                                 pattern_number=pattern_number
                                                                )
        
                pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                                   track=track,
                                                                                   pattern_number=pattern_number,
                                                                                   target_notes_to_turn_off=True
                                                                                  )
            # [E] Edit key - Edit selected note's length:
            if key == '3':
                edit_key(keypad, song_data, pattern_number, 
                         midi_and_channel, selected_beat,
                         track, selected_note_and_octave
                        )
                pattern = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                 track=track, 
                                                                 pattern_number=pattern_number
                                                                )
        
                pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                                   track=track,
                                                                                   pattern_number=pattern_number,
                                                                                   target_notes_to_turn_off=True
                                                                                  )
            # [C] - clear key:
            if key == '0':
                #selected_menu_button is selected to 15, to disable cursor or button selection on GUI
                screen_matrix = get_screen_matrix(song_data, pattern_number, midi_and_channel, 
                                                  selected_note_and_octave, selected_beat, pattern[:], 
                                                  selected_menu_button=15 
                                                 )
                clear_key(song_data, pattern_number, midi_and_channel, 
                          selected_note_and_octave, selected_beat, 
                          track, screen_matrix, keypad
                         )

                pattern = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                 track=track, 
                                                                 pattern_number=pattern_number
                                                                )
        
                pattern_notes_to_turn_off = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                                   track=track,
                                                                                   pattern_number=pattern_number,
                                                                                   target_notes_to_turn_off=True
                                                                                   )                                                                  
            # volume down/up note:
            if key == '7' or key == '9':
                volume_up_down_keys(key, song_data, pattern, pattern_number, 
                                    selected_beat, selected_note_and_octave, track
                                   )
                pattern = song_data.pianoroll_pattern_operations(operation='get pattern for single track', 
                                                                 track=track, 
                                                                 pattern_number=pattern_number
                                                                )
            # Menu key:
            if key == '#':
                # if in menu there is new pattern selected or pattern is cloned, then close this pattern, return new pattern number to playlist
                # then playlist will open selected pattern:
                new_pattern_number = menu(keypad, song_data, pattern_number, midi_and_channel, 
                                          selected_note_and_octave, selected_beat, pattern, pattern_notes_to_turn_off,
                                          track
                                         )
                if new_pattern_number is not None:
                    return new_pattern_number
            # when key was pressed, update GUI displayed:
            tui(song_data, pattern_number, midi_and_channel,
                selected_note_and_octave, selected_beat,
                pattern[:], selected_menu_button=None
               )

if __name__ == '__main__':
    song_data = SongData()
    keypad = Keypad()
    main(keypad, song_data, 1, 'M1c1', 1)