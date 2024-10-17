from tui.txtcolor import text_bg_color
from tui.txtcolor import text_font_color


def draw_slider(screen_matrix, y_position, title, percents, is_slider_selected=False):
    GUI_HEIGHT = 17
    GUI_WIDTH = 64

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
            if is_slider_selected:
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
            if is_slider_selected:
                char = text_bg_color('blue', text_font_color("black", RIGHT_POINTING_ARROW))
            else:
                continue
        else:
            char = ' '
        screen_matrix[y_position][start_x+i] = char

    if is_slider_selected:
        screen_matrix[y_position][4] = text_bg_color('blue', CURSOR)

    # Print silder's name below it:
    title = title + ': ' + str(percents) + '%'
    for i in range(len(title)):
        screen_matrix[y_position+1][start_x+i+1] = screen_matrix[y_position+1][start_x+i+1].replace(' ', title[i])

def draw_sliders(screen_matrix, which_slider_selected, option_params):
    keys = [*option_params]
    for k in range(len(keys)):
        title = keys[k]
        percents = option_params[keys[k]]
        y_position = 3 + 3*k

        if k == which_slider_selected:
            is_slider_selected = True
        else:
            is_slider_selected = False
        draw_slider(screen_matrix, y_position, title, percents, is_slider_selected)
