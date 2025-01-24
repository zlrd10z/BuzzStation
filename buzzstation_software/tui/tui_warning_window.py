from .scrmx import create_screen_matrix, print_screen_matrix, fill_matrix
from .txtcolor import text_bg_color, text_font_color
import os


BOLD = '\033[1m'
RESET = '\033[0m'

# Lambdas:
bold_text = lambda text: f'{BOLD}{text}{RESET}'
formatTextAsSelected = lambda text: text_bg_color('grey', text_font_color('black', text))

# Screen size (in characters):
screen_x = 64
screen_y = 16

# Window size:
window_size_y = int(16 / 2)
window_size_x = window_size_y * 5

# start printing poistion, so the window will be centred:
start_x = ((screen_x - window_size_x) / 2) -1
start_y = ((screen_y - window_size_y) / 2) -1

start_x = int(start_x)
start_y = int(start_y)

def draw_window(screen_matrix):
    for y in range(window_size_y):
        for x in range(window_size_x):
            if x == 0 and y == 0:
                single_char = '┌'
            elif x == 0 and y == window_size_y - 1:
                single_char = '└'
            elif x == window_size_x - 1 and y == 0:
                single_char = '┐'
            elif x == window_size_x - 1 and y == window_size_y - 1 :
                single_char = '┘'
            elif x == 0 and y == window_size_y - 3:
                single_char = '├'
            elif x == window_size_x - 1 and y == window_size_y - 3 :
                single_char = '┤'
            elif y == window_size_y - 3:
                single_char = '─'
            elif start_x + x == start_x or start_x + x == window_size_x + start_x - 1:
                single_char = '│'
            elif start_y + y == start_y or start_y + y == window_size_y + start_y - 1:
                single_char = '─'
            else:
                single_char = ' '
            
            screen_matrix[start_y+y][start_x+x] = text_bg_color(color='blue', text=single_char)
    return screen_matrix

# Put text 'Warning!' in window:
def draw_warning_txt(screen_matrix):
    warning_string = 'Warning!'
    x_start_print_text = start_x + (window_size_x - len(warning_string))/2
    x_start_print_text = int(x_start_print_text)

    for i in range(len(warning_string)):
        single_char = warning_string[i]
        single_char = bold_text(single_char)
        screen_matrix[start_y + 1][x_start_print_text + i] = text_bg_color('blue', single_char)
    
    return screen_matrix

# Draw ok/no buttons:
def draw_buttons(screen_matrix, ok_selected):
    ok_string = 'yes'
    no_string = 'no'
    
    distance_from_window_frame = 8
    x_ok_string_print_start = start_x + distance_from_window_frame
    x_no_string_print_start = start_x + window_size_x - distance_from_window_frame - len(no_string)

    for i in range(len(ok_string)):
        single_char = ok_string[i]
        single_char = bold_text(single_char)
        if ok_selected == True: 
            single_char = formatTextAsSelected(single_char)
        screen_matrix[start_y + window_size_y - 2][x_ok_string_print_start + i] = text_bg_color('blue', single_char)
    
    for i in range(len(no_string)):
        single_char = no_string[i]
        single_char = bold_text(single_char)
        if ok_selected == False: 
            single_char = formatTextAsSelected(single_char)
        screen_matrix[start_y + window_size_y - 2][x_no_string_print_start + i] = text_bg_color('blue', single_char)
    
    return screen_matrix

def draw_ok(screen_matrix):
    ok_string = 'ok'
    start_ok_x = int((start_x - len(ok_string)) / 2)
    for i in range(len(ok_string)):
        single_char = ok_string[i]
        single_char = bold_text(single_char)
        single_char = formatTextAsSelected(single_char)
        screen_matrix[start_y + window_size_y - 2][start_ok_x + i] = text_bg_color('blue', single_char)
    return screen_matrix

# Put info text in window:
def draw_info_txt(screen_matrix, action_warning):
    if action_warning == 'new song':
        info_text = 'Are you sure you want to start new project? If it\'s not saved, the entire progress will be lost!'
    elif action_warning == 'clear pattern':
        info_text = 'Are you sure you want to clear this entire pattern? It\'s not reversible!'
    elif action_warning == 'load song':
        info_text = 'Are you sure you want to load other song? If it\'s not saved, the entire progress will be lost!'
    elif action_warning == 'clear track':
        info_text = 'Are you sure you want to clear this entire track? It\'s not reversible!'
    elif action_warning == 'clear all tracks':
        info_text = 'Are you sure you want to clear all of the tracks? It\'s not reversible!'
    elif action_warning == 'clear selected':
        info_text = 'Are you sure you want to clear patterns from selection-start to current cursor position? It\'s not reversible!'
    elif action_warning == 'overwrite song':
        info_text = 'Are you sure you want to overwrite this song?'
    
    window_usable_length = window_size_x - 2
    
    sliced_texts = []
    x_start_print_text = []
    
    # Fit text to window:
    while len(info_text) > 0:
        x = 0
        while True:
            if len(info_text) > window_usable_length - x:
                last_char = info_text[window_usable_length - x - 1]
            else:
                last_char = ' '
            
            if last_char != ' ': 
                x += 1
            else: 
                sliced_text = info_text[:window_usable_length - x]
                if sliced_text[-1] == ' ':
                    sliced_texts.append(sliced_text[:-1])
                else:
                    sliced_texts.append(sliced_text)
                    
                x_start = start_x + int( (window_usable_length - len(sliced_text)) / 2 )
                x_start_print_text.append(x_start)
                info_text = info_text[window_usable_length - x:]
                break
                
    for i in range(len(sliced_texts)):
        if sliced_texts[i][0] == ' ':
            sliced_texts[i] = sliced_texts[i][1:]
        
        if sliced_texts[i][-1] == ' ':
            sliced_texts[i] = sliced_texts[i][:-1]
    
    for y in range(len(sliced_texts)):
        for x in range(len(sliced_texts[y])):
            #print(x_start_print_text[y] + x)
            screen_matrix[2 + y + start_y][x_start_print_text[y] + x + 2] = text_bg_color('blue', sliced_texts[y][x])
    
    return screen_matrix

def main(screen_matrix, ok_selected, action, error=False):
    screen_matrix = draw_window(screen_matrix)
    screen_matrix = draw_warning_txt(screen_matrix)
    if error:
        screen_matrix = draw_ok(screen_matrix)
    else:
        screen_matrix = draw_buttons(screen_matrix, ok_selected)
    screen_matrix = draw_info_txt(screen_matrix, action)
    print_screen_matrix(screen_matrix)
