from gui.txtcolor import text_bg_color
from gui.txtcolor import text_font_color

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

def draw_slider(screen_matrix, y_position, title, percents, slider_selected=False):
    '''
    There's 100 percent scale, 1 percent is represented as '▌'' char,
    2 percent as '█''.
    '''
    HALF_BLOCK = '▌'
    FULL_BLOCK = '█'
    RIGHT_POINTING_ARROW = '►'
    LEFT_POINTING_ARROW = '◄'
    CURSOR = '➤'

    #64 - width of the screen, 50 - width of slider
    start_x = (GUI_WIDTH - 50) / 2
    start_x = int(start_x)

    percents_scaled = int(percents / 2)
    od_number = False
    if percents % 2 == 1:
        percents_scaled += 1

    for i in range(0, 52):
        char = None
        if i == 0:
            if slider_selected:
                char = text_bg_color('blue', text_font_color("black", LEFT_POINTING_ARROW))
            else:
                continue
        elif i < percents_scaled:
            char = FULL_BLOCK
        elif i == percents_scaled:
            if percents % 2 == 1:
                char = HALF_BLOCK
            else:
                char = FULL_BLOCK
        elif i == 51:
            if slider_selected:
                char = text_bg_color('blue', text_font_color("black", RIGHT_POINTING_ARROW))
            else:
                continue
        else:
            char = ' '
        screen_matrix[y_position][start_x+i] = char

    if slider_selected:
        screen_matrix[y_position][4] = text_bg_color('blue', CURSOR)

    # Print silder's name below it:
    title = title + ': ' + str(percents) + '%'
    for i in range(len(title)):
        screen_matrix[y_position+1][start_x+i+1] = screen_matrix[y_position+1][start_x+i+1].replace(' ', title[i])

# create string from chars matrix (screen_matrix) and print it out
def print_screen_matrix(screen_matrix):
    frame = ''
    for i in range(len(screen_matrix)):
        for j in range(len(screen_matrix[0])):
            frame += screen_matrix[i][j]
    print(frame)
