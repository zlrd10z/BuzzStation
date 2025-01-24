from tui.txtcolor import text_font_color, text_bg_color
from tui.scrmx import create_screen_matrix
from tui.scrmx import fill_matrix
from tui.scrmx import print_screen_matrix
import os


# Format text as selected:
selected_text = lambda text: text_bg_color('grey', text_font_color('black', text))
clear_screen = lambda: os.system('clear')

def draw_window(screen_matrix, midi_instruments, instrument_type, midi_output, selected, currently_selected_midi_instrument):
    # Draw box with space on top for text:
    for y in range(len(screen_matrix)):
        for x in range(len(screen_matrix[y])):
            if x == 0 or x == len(screen_matrix[y]) - 1:
                screen_matrix[y][x] = text_bg_color('blue', '┃')
                if y == 0 or y == len(screen_matrix) - 1:
                    screen_matrix[y][x] = text_bg_color('blue', ' ')
                if x == 0 and y == 1:
                    screen_matrix[y][x] = text_bg_color('blue', '┏')
                if x == len(screen_matrix[y]) - 1 and y == 1:
                    screen_matrix[y][x] = text_bg_color('blue', '┓')
                if x == 0 and y == len(screen_matrix) - 2:
                    screen_matrix[y][x] = text_bg_color('blue', '┗')
                if x == len(screen_matrix[y]) - 1 and y == len(screen_matrix) - 2:
                    screen_matrix[y][x] = text_bg_color('blue', '┛')
            elif y == 1 or y == len(screen_matrix) - 2:
                screen_matrix[y][x] = text_bg_color('blue', '━')
                
            else:
                screen_matrix[y][x] = text_bg_color('blue', ' ')

    # Put title text on the screen:
    channel = midi_output[3:]
    text = 'Select new instrument for MIDI ' + midi_output[1] + ' Channel ' + channel + ':'
    
    #Center text on screen:
    text_start = (len(screen_matrix[0]) - len(text)) / 2
    text_start = int(text_start) 
    
    for i in range(len(text)):
        screen_matrix[0][text_start + i] = text_bg_color('blue', text[i])
    
    # Print info about currently selected midi instrument:
    text2 = 'Currently selected: ' + currently_selected_midi_instrument 
    
    for i in range(len(text2)):
        screen_matrix[-1][i] = text_bg_color('blue', text2[i])
    
    to_print = None
    if instrument_type == None:
        to_print = list(midi_instruments.keys())
        if selected > 11:
            to_print = ['…'] + to_print[12:]
            selected -= 11
        else:
            to_print = to_print[:13]
            to_print[-1] = '…' 
    else:
        to_print = list(midi_instruments[instrument_type].keys())

    y = 2
    x = 1
    for i in range(len(to_print)):
        for j in range(len(to_print[i])):
            if i == selected:
                screen_matrix[y + i][x + j] = selected_text(to_print[i][j])
            else:
                screen_matrix[y + i][x + j] = text_bg_color('blue', to_print[i][j])
                
def main(midi_instruments, midi_output, selected, currently_selected_midi_instrument, instrument_type=None):
    screen_matrix = create_screen_matrix()
    screen_matrix = fill_matrix(screen_matrix)
    draw_window(screen_matrix, midi_instruments, instrument_type, midi_output, selected, currently_selected_midi_instrument)
    print_screen_matrix(screen_matrix)
