from .txtcolor import text_font_color
from .txtcolor import text_bg_color
import os
from .scrmx import create_screen_matrix
from .scrmx import fill_matrix
from .scrmx import print_screen_matrix


# Lambdas:
clear_screen = lambda: os.system('clear')
underlined_text = lambda text: (f'\033[4m{text}\033[0m')

# 64x18 characters:
tui_height = 17 #terminal command line is taking one line
tui_width = 64

def draw_frame(screen_matrix):
    for i in range(len(screen_matrix)):
        for j in range(len(screen_matrix[i])):
            if i < 1 or i > len(screen_matrix) - 4:
                screen_matrix[i][j] = text_bg_color('blue', ' ')
                
            elif j < 2 or j > len(screen_matrix[i]) - 8:
                screen_matrix[i][j] = text_bg_color('blue', ' ')
                screen_matrix[i][j] = text_bg_color('blue', ' ')

            else:
                screen_matrix[i][j] = ' '
    return screen_matrix

# Draw vertical lines in different color tone then already used for better visibility:
def draw_vertical_lines(screen_matrix):
    x_position = 9
    x = 0
    
    for i in range(8):
        for j in range(13):
            for k in range(3):
                screen_matrix[13-j][x_position + x + k] = text_bg_color('black grey', ' ')
        x += 6
    return screen_matrix

# Draw horizontal lines in different color tone  then already used for better visibility:
def draw_horizontal_lines(screen_matrix):
    y_position = 2
    x_position = 9
    counter = 0
    is_light_grey = True 
    
    for i in range(6):
        for j in range(16*3):
            if counter == 3:
                if is_light_grey: is_light_grey = False
                else: is_light_grey = True
                counter = 0
                
            if is_light_grey:
                char = text_bg_color('light grey', ' ')
            else:
                char = text_bg_color('dark grey', ' ')
            screen_matrix[y_position + 2 * i][x_position + j] = char
            counter += 1
            
    return screen_matrix

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
notes_displayed = []


def draw_part_of_piano(screen_matrix, y_position, x_poistion, octave, 
                       selected_note, start_note=0, counter=0, note_already_selected=False
):    
    for i in range(12):
        note = ' '
        note_index = start_note + i
        if note_index > 11 or counter > 12: 
            break
        notes_displayed.append(notes[note_index] + str(octave))
    
        # string with note and octave has to be in length of 3 characters:
        if len(notes[note_index]) == 2:
            note = notes[note_index] + str(octave)
        else:
            note += notes[note_index] + str(octave)
        
        counter += 1
        
        for j in range(4):
            # draw first 4 chars which makes piano key:
            if len(notes[note_index]) > 1:
                pass # drawing back keys
            else:
                screen_matrix[y_position - i][j+x_poistion] = text_bg_color('grey', ' ')
                # drawing part of white keys:
                
            if j == 0:
                pass
            else:
                # draw last 3 chars which makes piano key:
                # drawing key and note on key:
                note_part = text_font_color('black', note[j-1])
                note_part = text_bg_color('grey', note_part)
                if not note_already_selected and  selected_note in note:
                    if note[j-1] != ' ':
                        note_part = underlined_text(note_part)
                        if j == 3:
                            note_already_selected = True
                
                screen_matrix[y_position - i][j+x_poistion+3] = note_part
    return counter, screen_matrix, note_already_selected

def draw_piano(screen_matrix, octave, start_note, selected_note):
    x = draw_part_of_piano(screen_matrix = screen_matrix, 
                            y_position = 13, 
                            x_poistion = 2, 
                            octave = octave, 
                            start_note = start_note,
                            selected_note = selected_note)
    
    counter = x[0]
    screen_matrix = x[1]
    was_note_underlined = x[2]
    screen_matrix = draw_part_of_piano(screen_matrix=screen_matrix, 
                                        y_position=13 - counter, 
                                        x_poistion=2, 
                                        octave=octave + 1, 
                                        counter=counter,
                                        selected_note=selected_note,
                                        note_already_selected=was_note_underlined
                                        )[1]
    return screen_matrix

def draw_quarter_time(screen_matrix):
    x_position = 9
    x = 0
    for i in range(16):
        char_number = chr(0x2488 + i)
        if i % 4 == 0:
            screen_matrix[0][x_position + x] = text_font_color('black', text_bg_color('blue', char_number))
        else:
            screen_matrix[0][x_position + x] = text_bg_color('blue', char_number)
        x += 3
    return screen_matrix

def draw_pattern_number(screen_matrix, pattern_number=1):
    text_to_print = 'Pattern: ' + str(pattern_number)
    axisx_start_printing = (tui_width - len(text_to_print)) - 2
    for i in range(len(text_to_print)):
        screen_matrix[tui_height-1][axisx_start_printing + i] = text_bg_color('blue', text_to_print[i])

    return screen_matrix

#draw Swing value, BPM value and MIDI output and channel number
def draw_swing_bpm_midi(screen_matrix, bpm_value=100, swing_value=40, channel_number=1):
    text_to_print = 'BPM: ' + str(bpm_value) + (9 - len(str(bpm_value))) * ' '
    text_to_print += 'Swing: ' + str(swing_value) + (9 - len(str(swing_value))) * ' ' 
    text_to_print += 'Channel: ' + str(channel_number)
    for i in range(len(text_to_print)):
        screen_matrix[tui_height-1][i+2] = text_bg_color('blue', text_to_print[i])
    return screen_matrix


def draw_play_pause(screen_matrix, is_playing=False, playing_mode=False):
    playing_info = 'Pause'
    x = 0
    if is_playing: 
        playing_info = 'Playing'
        x += 3
        
    if playing_mode:
        playing_sign = '[S]'
    else:
         playing_sign = '[P]'
        
    axisx_start_printing = int(tui_width / 2 - len(playing_info))

    if is_playing:
        axisx_start_printing -= 1

    for i in range(len(playing_info)):
        screen_matrix[tui_height-3][axisx_start_printing + 1 + i + x] = text_bg_color('blue', playing_info[i])

    for i in range(3):
        screen_matrix[0][59 + i] = text_bg_color('blue', playing_sign[i])
        
    return screen_matrix

def draw_buttons(screen_matrix, selected=None):
    button_playlist = ' Playlist '
    button_playing_mode = ' Playing mode '
    button_clone = ' Clone '
    button_previous_pattern = ' ⇽ '
    button_next_pattern = ' ⇾ '
    
    toDraw =  button_previous_pattern + '?' + button_playing_mode + '?' +  button_clone + '?' + button_next_pattern
    question_mark_counter = 0
    for i in range(len(toDraw)):
        if toDraw[i] == '?': 
            question_mark_counter += 1
            
        elif question_mark_counter == selected:
            screen_matrix[tui_height-2][16 + i] = text_bg_color('grey', toDraw[i])
        else:
            screen_matrix[tui_height-2][16 + i] = toDraw[i]
    return screen_matrix


def draw_notes_on_piano(screen_matrix, pattern=None):    
    x_position = 9
    y_position = 13
    if pattern is not None:
        # for 16 quarter notes:
        for i in range(16):
            # for each note in quareted (chord):
            for j in range(len(pattern[i])):
                if pattern[i][j][0] in notes_displayed:
                    y = y_position -  notes_displayed.index(pattern[i][j][0]) 
                    # quarter note displayed as 3 character square:
                    for k in range(pattern[i][j][1] * 3 - 1):            
                        single_char = chr(0x2580 + pattern[i][j][2])
                        screen_matrix[y][x_position + i + k] = screen_matrix[y][x_position + i + k].replace(' ', single_char)


            x_position += 2
    return screen_matrix

def draw_cursor(screen_matrix, cursor, position, note_length_edit):
    x_position = 9
    y_position = 13
    
    octave = cursor[-1:]
    note = cursor.replace(octave, '')
    y = y_position - notes_displayed.index(cursor)
    x = x_position + position * 3
    cursor_char = '☟'
    
    if note_length_edit:
        cursor_char = '↔'
    
    if ' ' in screen_matrix[y-1][x]:
        screen_matrix[y-1][x] = screen_matrix[y-1][x].replace(' ', cursor_char)
    else:
        for i in range(8):
            if chr(0x2581 + i) in screen_matrix[y-1][x]:
                screen_matrix[y-1][x] = screen_matrix[y-1][x].replace(chr(0x2581 + i), cursor_char)
                break
                
        for i in range(16):
            if chr(0x2488 + i) in screen_matrix[y-1][x]:
                screen_matrix[y-1][x] = screen_matrix[y-1][x].replace(chr(0x2488 + i), cursor_char)
                break
    
    return screen_matrix
    
def get_starting_note_and_octave(selected_note):
    global notes_displayed
    octave = int(selected_note[-1:])
    note = selected_note
    note = note.replace(str(octave), '')
    
    if len(notes_displayed) > 0:
        if selected_note in notes_displayed:
            if notes_displayed.index(selected_note) + 2 < len(notes_displayed):
                start_note = notes.index(notes_displayed[0][:-1])
                octave = int(notes_displayed[0][-1])
    
            elif notes_displayed.index(selected_note) + 2 == len(notes_displayed):
                start_note = notes.index(notes_displayed[1][:-1])
                octave = int(notes_displayed[1][-1])

        else:
            start_note = notes.index(note)
    
    else:
        octave = 5
        start_note = 0

    notes_displayed = []
    return start_note, octave

# draw indicators that there are more notes beside the displayed octave(s):
def draw_indicators(screen_matrix, pattern):
    above = False
    below = False
    
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if pattern[i][j][0] not in notes_displayed:
                if int(pattern[i][j][0][-1]) >= int(notes_displayed[-1][-1]):
                    above = True
                if int(pattern[i][j][0][-1]) <= int(notes_displayed[0][-1]):
                    below = True
                    
    if above:
        screen_matrix[1][57] = text_bg_color('blue', '⇡')
    if below:
        screen_matrix[13][57] = text_bg_color('blue', '⇣')
    
    return screen_matrix

def draw_midi_info(screen_matrix, midi_output_and_channel):
    midi_output = midi_output_and_channel[1]
    midi_channel = midi_output_and_channel[3:]
    
    for i in range(5):
        screen_matrix[5][58 + i] = text_bg_color('blue', ('MIDI' + midi_output)[i])

    channel_string = 'Ch: '
    if len(midi_channel) == 2:
        channel_string = 'Ch:'
        
    for i in range(len(channel_string + midi_channel)):
        screen_matrix[6][58 + i] = text_bg_color('blue', (channel_string + midi_channel)[i])

    return screen_matrix
        
def main(bpm_value, swing_value, pattern_number, playing_mode, 
     playing=False, midi_output_and_channel='M1c16', selected_note=None, 
     selecteded_beat=None, pattern=None, selected_menu_button=None, 
     print_it=True, note_length_edit=False
):
        
    start_note, octave = get_starting_note_and_octave(selected_note)

    channel_number = midi_output_and_channel[3:]
    
    screen_matrix = create_screen_matrix()
    screen_matrix = fill_matrix(screen_matrix)
    screen_matrix = draw_frame(screen_matrix)
    screen_matrix = draw_vertical_lines(screen_matrix)
    screen_matrix = draw_horizontal_lines(screen_matrix)
    screen_matrix = draw_piano(screen_matrix, octave, start_note, selected_note)
    screen_matrix = draw_quarter_time(screen_matrix)
    screen_matrix = draw_pattern_number(screen_matrix, pattern_number)
    screen_matrix = draw_swing_bpm_midi(screen_matrix, bpm_value, swing_value, channel_number)
    screen_matrix = draw_play_pause(screen_matrix, playing, playing_mode)
    screen_matrix = draw_buttons(screen_matrix, selected_menu_button)
    if pattern is not None:
        screen_matrix = draw_notes_on_piano(screen_matrix, pattern = pattern)
    if selected_menu_button is None:
        screen_matrix = draw_cursor(screen_matrix, selected_note, selecteded_beat, note_length_edit)
    screen_matrix = draw_midi_info(screen_matrix, midi_output_and_channel)
    screen_matrix = draw_indicators(screen_matrix, pattern)
    if print_it:
        print_screen_matrix(screen_matrix)
    else:
        return screen_matrix


    
if __name__ == '__main__':
    # Tests
    def create_example_pattern():
        pattern = []
        for i in range(16):
            l = []
            pattern.append(l)

        #                   note, note length, volume
        pattern[0].append(['C5', 1, 8])
        pattern[0].append(['D#5', 1, 8])
        pattern[0].append(['F5', 1, 2])
        pattern[1].append(['C#5', 1, 1])
        pattern[4].append(['C#5', 3, 4])
        
        pattern[0].append(['A#5', 1, 1])
        pattern[1].append(['A#5', 1, 1])
        pattern[2].append(['A#5', 1, 2])
        pattern[3].append(['A#5', 1, 3])
        pattern[4].append(['A#5', 1, 4])
        pattern[5].append(['A#5', 1, 5])
        pattern[6].append(['A#5', 1, 6])
        pattern[7].append(['A#5', 1, 7])
        pattern[8].append(['A#5', 1, 8])
        
        return pattern

    example_pattern = create_example_pattern()
    print(example_pattern)
    main(bpm_value=111, swing_value=31, pattern_number=45, pattern=example_pattern, selected_note='A4', selecteded_beat=14, playing=False, playing_mode=False)
