from tui.txtcolor import text_bg_color
from tui.txtcolor import text_font_color
from tui.scrmx import print_screen_matrix


GUI_HEIGHT = 17
GUI_WIDTH = 64

## Draw window:
# Screen size (in characters):
screen_x = 64
screen_y = 16

# Window size:
window_size_y = 14
window_size_x = 44

# start printing poistion, so the window will be centred:
win_start_x = ((screen_x - window_size_x) / 2) - 1
win_start_y = ((screen_y - window_size_y) / 2) - 1

win_start_x = int(win_start_x)
win_start_y = int(win_start_y)

def draw_window_bg(screen_matrix):
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
            elif x == 0 and (y == 2 or y == 5 or y == 9):
                single_char = '├'
            elif x == window_size_x - 1 and (y == 2 or y == 5 or y == 9) :
                single_char = '┤'
            elif win_start_x + x == win_start_x or win_start_x + x == window_size_x + win_start_x - 1:
                single_char = '│'
            elif (
                  (win_start_y + y == win_start_y) 
                  or (win_start_y + y == window_size_y + win_start_y - 1)
                  or (y == 2)
                  ):
                single_char = '─'
            elif y == 5 or y == 9:
                single_char = '╌'
            else:
                single_char = ' '    
            screen_matrix[win_start_y+y][win_start_x+x] = text_bg_color(color='blue', text=single_char)
    return screen_matrix

def draw_title(screen_matrix):
    ## Put Title:
    title = 'Menu'
    title_start_x = (window_size_x - len(title)) / 2
    title_start_x = int(title_start_x) + win_start_x
    for i in range(len(title)):
        one_char = title[i]
        one_char = f'\033[1m{one_char}\033[0m'
        screen_matrix[win_start_y+1][title_start_x+i] = text_bg_color(color='blue', text=one_char)
    return screen_matrix

def draw_info(screen_matrix):
    txt = 'Move cursor to:'
    for i in range(len(txt)):
        char = txt[i]
        screen_matrix[win_start_y+3][win_start_x+i+15] = text_bg_color(color='blue', text=char)

def draw_one_button(screen_matrix, text, y, x, selected=False):
    x += win_start_x
    y += win_start_y
    for i in range(len(text)):
        one_char = text[i]
        if selected:             
            one_char = text_font_color(color='black', text=one_char)
            screen_matrix[y][x+i] = text_bg_color(color='grey', text=one_char)
        else:
            screen_matrix[y][x+i] = one_char

def draw_buttons(screen_matrix, selected_button):
    buttons = [
                ['+16lvl', 4, 9],
                ['-16lvl', 4, 16],
                ['Begining', 4, 23],
                ['End', 4, 32],
                ['Select', 6, 14],
                ['Unselect', 6, 21],
                ['CopyPaste', 8, 3],
                ['Undo', 8, 13],
                ['Clear Selected Patterns', 8, 18],
                ['Save Song', 10, 8],
                ['Load Song', 10, 18],
                ['New Song', 10, 28],
                ['Clear Enitre Playlist', 12, 11],
              ]

    for button_attr in buttons:
        selected = False
        if button_attr[0] == selected_button:
            selected = True
        text, y, x = button_attr
        draw_one_button(screen_matrix, text, y, x, selected)

def display_menu_window(screen_matrix, selected_button, selection, list_of_instruments):
    draw_window_bg(screen_matrix)
    draw_title(screen_matrix)
    draw_info(screen_matrix)
    draw_buttons(screen_matrix, selected_button)
    print_screen_matrix(screen_matrix)
