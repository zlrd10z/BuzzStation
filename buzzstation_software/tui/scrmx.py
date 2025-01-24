from tui.txtcolor import text_bg_color
from tui.txtcolor import text_font_color
import os


GUI_HEIGHT = 17
GUI_WIDTH = 64

# Create matrix 16 x 64 chars
def create_screen_matrix():
    screen_matrix = []
    for i in range(GUI_HEIGHT):
        screen_matrix.append([])
    return screen_matrix

# Append matrix with spaces characters:
def fill_matrix(screen_matrix):
    for i in range(GUI_HEIGHT):
        for j in range(GUI_WIDTH):
            screen_matrix[i].append(' ')
    return screen_matrix

# Fill screen matrix with color
def bg_color(screen_matrix):
    for y in range(len(screen_matrix)):
        for x in range(len(screen_matrix[y])):
            screen_matrix[y][x] = text_bg_color('blue' ,' ')
    return screen_matrix

def draw_box(screen_matrix):
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

# Draw centered text at the bottom of the screen:
def draw_title(screen_matrix, text):
    width = len(screen_matrix[0])
    start_print = (width - len(text)) / 2
    start_print = int(start_print)
    for i in range(len(text)):
        screen_matrix[0][start_print+i] = screen_matrix[0][start_print+i].replace(' ', text[i])

#draw text on the bottom alligned to the left:
def draw_instr(screen_matrix, info_text):
    for i in range(len(info_text)):
        screen_matrix[len(screen_matrix)-1][i+1] = screen_matrix[len(screen_matrix)-1][i+1].replace(' ', info_text[i])

# create string from chars matrix (screen_matrix) and print it out
def print_screen_matrix(screen_matrix, debug=False):
    if not debug:
        frame = ''
        print('\033[H', end='')
        for i in range(len(screen_matrix)):
            for j in range(len(screen_matrix[0])):
                frame += screen_matrix[i][j]
            frame = (15-i)*'\033[F' + '\033[K' + frame
            print(frame, flush=True)
            frame = ''
    elif debug:
        frame = ''
        for i in range(len(screen_matrix)):
            for j in range(len(screen_matrix[0])):
                frame += screen_matrix[i][j]
            print(frame)
            frame = ''



def clear_screen():
    print('\033[H', end='')