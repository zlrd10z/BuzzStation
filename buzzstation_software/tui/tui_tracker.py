import os, sys
import time
from .txtcolor import text_bg_color
from .txtcolor import text_font_color
from .scrmx import create_screen_matrix
from .scrmx import fill_matrix
from .scrmx import print_screen_matrix


# Lambdas:
clear_screen = lambda: os.system('clear')
formatTextAsSelected = lambda text: text_bg_color('grey', text_font_color('black', text))

# 64x18 characters:
tui_height = 17 #terminal command line is taking one line
tui_width = 64

# This function: 
# Draws numbers on the left, from 1-16, which represents quaternotes in pattern
# Draws 1char-width frames which separates 8 tracks
# Fills with solid color part of right part of the screen, which create space for other information like actual BPM value
def draw_frames_and_numbers(first_number, screen_matrix):
    for i in range(16):
        id_number = str(first_number + i)
        #print(id_number)
        i += 1
        # Draw Numbers 1-16
        if(len(id_number) > 1):    
            screen_matrix[i][0] = text_bg_color('blue', id_number[0])
            screen_matrix[i][1] = text_bg_color('blue', id_number[1])
            # Mark each bar with yellow:
            if int(id_number) % 4 == 1:
                screen_matrix[i][0] = text_font_color('black', screen_matrix[i][0])
                screen_matrix[i][1] =  text_font_color('black', screen_matrix[i][1])
        else:
            screen_matrix[i][1] = text_bg_color('blue', id_number)
            screen_matrix[i][0] = text_bg_color('blue', ' ')
            if int(id_number) % 4 == 1: 
                screen_matrix[i][1] = text_font_color('black', screen_matrix[i][1])

        # Draw horizontal frame at the top on the screen:
        # On that line, there will be displayed names of samples, assigned to each track
        for j in range(len(screen_matrix[0])):
            screen_matrix[0][j] = text_bg_color('blue', ' ')

        # Draw vertical frames and fill on the right side:
        for j in range(len(screen_matrix)):
            tracks = 1
            for k in range(len(screen_matrix[0])):
                if(k % 6 == 1 and k > 1 and tracks <= 8):
                    screen_matrix[j][k] = text_bg_color('blue', ' ')
                    tracks += 1
                elif(tracks > 8):
                    screen_matrix[j][k] = text_bg_color('blue', ' ')
    return screen_matrix

#mark tracks with assigned sample name:
def name_tracks(list_of_samples, screen_matrix, selected=None):
        # Samples are stored as path to file
        # Extracting names and abbreviate to first 4 letters with ellipsis on the end:
        for i in range(len(list_of_samples)):
            sample_path = list_of_samples[i]
            sample_path = sample_path.split('/')
            sample_name = sample_path[-1]
            sample_name = sample_name.split('.')
            sample_name = sample_name[0]
            if len(sample_name) > 5: 
                sample_name = sample_name[:4] + '…'
            list_of_samples[i] = sample_name

        if(len(list_of_samples) < 8):
            x = 8 - len(list_of_samples)
            for i in range(x):
                list_of_samples.append('Empty')

        tracks = 1
        for i in range(len(screen_matrix[0])):
            if(i % 6 == 2 and tracks <= 8):
                for j in range(5):
                    if j > len(list_of_samples[tracks-1])-1: break
                    if tracks-1 == selected and selected is not None:
                        screen_matrix[0][i+j] = text_bg_color('grey', list_of_samples[tracks-1][j])
                    else:
                        screen_matrix[0][i+j] = text_bg_color('blue', list_of_samples[tracks-1][j])
                tracks += 1
        return screen_matrix


def draw_notes(screen_matrix, pattern, selected_note_element=None):
    # Three is 8 tracks with length of 16, each note has 5 chars for note value and it's volume, between that note info there is 1 char of free space
    for i in range(16):
        x = 2
        for j in range(8):
            note = pattern[j][i]
            if len(note) > 0 and len(note[0]) < 3:
                note[0] += ' '

            if selected_note_element is None: selected_note_element = [None, None, None]

            if len(note) == 0:
                for k in range(5):    
                    if i == selected_note_element[1] and j == selected_note_element[0]:
                        screen_matrix[i+1][x+k] = formatTextAsSelected('.')
                    else:
                        screen_matrix[i+1][x+k] = '.'
            else:
                l = 0
                for k in range(5):
                    if k != 3: 
                        if k < 3:
                            # print note:
                            if selected_note_element[2] == 0 and i == selected_note_element[1] and j == selected_note_element[0]:
                                screen_matrix[i+1][x+k] = formatTextAsSelected(note[0][l])
                            else:
                                screen_matrix[i+1][x+k] = note[0][l]
                            l += 1
                            # print note's volume
                        else:
                            if selected_note_element[2] == 1 and i == selected_note_element[1] and j == selected_note_element[0]:
                                screen_matrix[i+1][x+k] = formatTextAsSelected(note[1])
                            else:
                                screen_matrix[i+1][x+k] = note[1]

            x += 6
    return screen_matrix

# Draw Vertical grey lines for better visibility:
def draw_vertical_lines(screen_matrix):
    # screen's hight of 17 characters:
    for y in range(17):
        track_position = 2
        # 8 tracks:
        for i in range(8):
            # 5 characters ength for track:
            for j in range(5):
                # y coordinate for 1, 5, 9, 13 beat:
                if y % 4 == 1:
                    screen_matrix[y][track_position + j] = text_bg_color('black grey', screen_matrix[y][track_position+j])
            track_position += 6
    
    return screen_matrix

                                   
def draw_song_name(screen_matrix, song_name=None):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = ' Song name:'
    # Draw 'Song Name:' text
    for i in range(tui_width-x):
        if i <= len(info_text)-1:
            screen_matrix[0][x+i] = text_bg_color('blue', info_text[i])

    if song_name is not None:
        # Center filename:
        if len(song_name) < tui_width - x:
            how_many_fill = tui_width - x - len(song_name)
            how_many_fill = int(how_many_fill/2 - 1)
            song_name = ' '*how_many_fill + song_name

        # Draw filename (max two lines):
        for j in range(2):
            for i in range(tui_width - x):
                if len(song_name) == 0: break

                #if name len exceed space for song name:
                if j == 1 and i == tui_width - x - 1 and len(song_name) > 1:
                    screen_matrix[1+j][x+i] = text_bg_color('blue', '…')
                else:
                    screen_matrix[1+j][x+i] = text_bg_color('blue', song_name[:1])
                    song_name = song_name[1:]
    return screen_matrix

def draw_pattern_number(screen_matrix, pattern_numer=1):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = ' Pattern: ' + str(pattern_numer)
    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[0][x + i] = text_bg_color('blue', info_text[i])
    return screen_matrix

def draw_bpm_vol_swing_values(screen_matrix, bpm_value, swing_value, vol_value):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 3 + 6*8
    info_text = 'BPM:    Swing:  bVOL:   '
    for i in range(3):
        value_to_print = 0
        match i:
            case 0: 
                value_to_print = bpm_value
            case 1: 
                value_to_print = swing_value
            case 2: 
                value_to_print = vol_value
        # swing can varries between -50% and 50%:
        if i == 1:
            if value_to_print < 0:
                sign = '-'
            else:
                sign = ' '
            value_to_print = str(abs(value_to_print))
            how_many_fills = 2 - len(value_to_print)
            value_to_print = sign + '0'*how_many_fills + value_to_print
        else:
            value_to_print = str(value_to_print)
            how_many_fills = 3 - len(value_to_print)
            value_to_print = '0'*how_many_fills + value_to_print


        for j in range(11):
            if j < 8:
                screen_matrix[1+i][x+j] = info_text[:1]
                info_text = info_text[1:]
            else:
                screen_matrix[1+i][x+j] = value_to_print[:1]
                value_to_print = value_to_print[1:]
    return screen_matrix

# Draw menu info and buttons:
def draw_menu(screen_matrix, selected=None):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = '    Menu: '
    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[5][x + i] = text_bg_color('blue', info_text[i])

    # previous button and next pattern buttons:
    text = 'pattern'
    for i in range(tui_width - x):
        if i <= len(text)-1:
            screen_matrix[6][x + i] = text_bg_color('blue', text[i])

    button_text = '⇽'
    for i in range(tui_width - x):
        if i <= len(button_text)-1:
            if selected == 0:
                screen_matrix[6][x+i+8] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[6][x+i+8] = button_text[i]


    button_text = '⇾'
    for i in range(tui_width - x):
        if i <= len(button_text)-1:
            if selected == 1:
                screen_matrix[6][x+i+11] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[6][x+i+11] = button_text[i]

    # playlist button:
    button_text = ' Clone '
    for i in range(tui_width - x):
        if i <= len(button_text) - 1:
            if selected == 2:
                screen_matrix[7][x+i+3] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[7][x+i+3] = button_text[i]

    # clone pattern:
    button_text = ' Clear '
    for i in range(tui_width - x):
        if i <= len(button_text)-1:
            if selected == 3:
                screen_matrix[8][x+i+3] = formatTextAsSelected(button_text[i])
            else: 
                screen_matrix[8][x+i+3] = button_text[i]

    return screen_matrix

# The screen fits max 8 tracks, so if there more samples, to display others, page should be toggled:
def draw_page(screen_matrix, page_number):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = 'Page: ' + str(page_number)
    how_many_fills = ((tui_width - x) - len(info_text))/2
    info_text = ' '*int(how_many_fills) + info_text

    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[15][x + i] = text_bg_color('blue', info_text[i])
    return screen_matrix
    
def draw_play_pause(screen_matrix, is_playing=False, playing_mode=False):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = 'Pause'
    if is_playing: 
        info_text = 'Playing'
    # Add information if Song or Pattern is played    
    if playing_mode:
        info_text += ' [S]'
    else:
        info_text += ' [P]'
    how_many_fills = ((tui_width - x) - len(info_text)) / 2
    info_text = ' ' * int(how_many_fills) + info_text

    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[16][x + i] = text_bg_color('blue', info_text[i])
    return screen_matrix

# Above the track there's just few letters for sample name, so it's abreviated, 
# when sample is selected, on the right side longer filename will be displayed:
def draw_samplename_long(screen_matrix, sample_path):
    if sample_path != 'Empty':
        sample_path = sample_path.split('/')
        sample_name = list(sample_path[-1])
    
    else:
        sample_name = list('  [No audio      file       assigned]')
    
    
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = 'Sample Name:'
    how_many_fills = ((tui_width - x) - len(info_text)) / 2
    info_text = ' ' * int(how_many_fills) + info_text

    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[10][x + i] = text_bg_color('blue', info_text[i])
            
    for j in range(3):
        for i in range(tui_width - x):
            if i <= len(info_text)-1:
                if len(sample_name) > 0:
                    screen_matrix[11 + j][x + i] = text_bg_color('blue', sample_name[0])
                    sample_name.pop(0)
                    
                    if j == 2 and i == (tui_width - x - 1):
                        if len(sample_name) > 0:
                            screen_matrix[11 + j][x + i] = text_bg_color('blue', '…')
                        
                    
                else: break
        if len(sample_name) == 0: break
                
    return screen_matrix

def draw_song_name(screen_matrix, song_name):
    song_name = song_name.split('/')
    song_name = list(song_name[-1])
    
    
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = 'Song Name:'
    how_many_fills = ((tui_width - x) - len(info_text)) / 2
    info_text = ' ' * int(how_many_fills) + info_text

    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[10][x + i] = text_bg_color('blue', info_text[i])
            
    for j in range(3):
        for i in range(tui_width - x):
            if i <= len(info_text)-1:
                if len(song_name) > 0:
                    screen_matrix[11+j][x+i] = text_bg_color('blue', song_name[0])
                    song_name.pop(0)
                    
                    if j == 2 and i == (tui_width - x - 1):
                        if len(song_name) > 0:
                            screen_matrix[11+j][x+i] = text_bg_color('blue', '…')
                        
                    
                else: break
        if len(song_name) == 0: break
                
    return screen_matrix

def main(list_of_samples, pattern, is_playing, bpm_value, 
         swing_value, playing_mode, vol_value, pattern_number, 
         song_name, selected_button=None, cursor=None, print_on_screen=True
):
    
    list_of_samples_full_paths = list_of_samples[:]
    full_selected_sample_name = list_of_samples_full_paths[cursor[0]]
    if cursor[0] < 8:
        page_number = 1
    else:
        page_number = 2
        cursor[0] -= 8
        pattern = pattern[-8:]
        list_of_samples = list_of_samples_full_paths[-8:]

    if cursor[1] == 0:
        selected_sample = cursor[0]
        selected_note_element = None
    else:
        selected_note_element = cursor[:]
        selected_note_element[1] -= 1
        selected_sample = None
        
    if selected_button is not None:
        selected_sample = None
        selected_note_element = None
    
    screen_matrix = create_screen_matrix()
    sceeen_matrix = fill_matrix(screen_matrix)
    screen_matrix = draw_frames_and_numbers(1, screen_matrix)
    screen_matrix = name_tracks(list_of_samples[:], screen_matrix, selected=selected_sample)
    screen_matrix = draw_pattern_number(screen_matrix, pattern_number)
    screen_matrix = draw_page(screen_matrix, page_number)
    screen_matrix = draw_notes(screen_matrix, pattern, selected_note_element)
    if selected_button is None:
        screen_matrix = draw_samplename_long(screen_matrix, full_selected_sample_name)
    if selected_button is not None and song_name != 'No songname':
        screen_matrix = draw_song_name(screen_matrix, song_name)
    screen_matrix = draw_vertical_lines(screen_matrix)
    screen_matrix = draw_bpm_vol_swing_values(screen_matrix, bpm_value, swing_value, vol_value)
    screen_matrix = draw_menu(screen_matrix, selected_button)
    screen_matrix = draw_play_pause(screen_matrix, is_playing, playing_mode)
    if print_on_screen == True:
        print_screen_matrix(screen_matrix)
    return screen_matrix


def create_example_pattern():
    example_pattern = []
    
    # append 16 tracks:
    for i in range(16):
        track = []
        example_pattern.append(track)
    
    # append 16 notes in 16 tracks:
    for i in range(16):
        for j in range(16):
            note = []
            example_pattern[i].append(note)
    
    # append kick 4x4 with full volume - hex F
    for i in range(16):
        if i % 4 == 0:
            example_pattern[0][i] = ['C5', 'F']
    
    # append snare:
    for i in range(16):
        if i % 4 == 0 and i > 1 and i != 8:
            example_pattern[1][i] = ['C5', '9']
    
    return example_pattern

if __name__ == '__main__':
    # Tests
    example_pattern = create_example_pattern()
    main(list_of_samples = ['folder/kick_deep_132.mp3', 'a'], pattern = example_pattern, selected_note_element = [1, 3, 3])
    print(example_pattern[0])

    
#
#selected_note_element = [3, 1, 2])
#3track, if there would be three tracks: kick snare hihat, the hihat would be choosen
#1 - first note
#2 - selected quarter note's volume
