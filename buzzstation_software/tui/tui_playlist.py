from .tui_tracker import create_screen_matrix, fill_matrix, draw_frames_and_numbers, name_tracks, print_screen_matrix, draw_bpm_vol_swing_values
from .txtcolor import text_bg_color, text_font_color
import os

clear_screen = lambda: os.system('clear')
formatTextAsSelected = lambda text: text_bg_color('grey', text_font_color('black', text))

#Create vertical lines for better visibility:
def draw_vertical_lines(screen_matrix):
    # screen's hight of 17 characters:
    for y in range(17):
        track_position = 2
        # 8 tracks:
        for i in range(8):
            # 5 characters ength for track:
            for j in range(5):
                # each second i
                if y % 2 == 1:
                    screen_matrix[y][track_position + j] = text_bg_color('black grey', screen_matrix[y][track_position + j])
            track_position += 6
    return screen_matrix

# Draw information that it is plalist:
def draw_info_mode(screen_matrix):
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = ' [Playlist]' 
    # Draw 'Song Name:' text
    for i in range(64 - x):
        if i <= len(info_text)-1:
            screen_matrix[0][x + i] = text_bg_color('blue', info_text[i])
    return screen_matrix

# Draw menu texts and buttons:
def draw_menu(screen_matrix, selected = None):
    tui_width = 64
    # x is char on x axis, where the tracks ends, and the song info starts:
    x = 2 + 6*8
    info_text = '    Menu: '
    # Draw 'Song Name:' text
    for i in range(tui_width - x):
        if i <= len(info_text)-1:
            screen_matrix[5][x + i] = text_bg_color('blue', info_text[i])

    # playlist buttons:
    button_text = ' Save '
    for i in range(tui_width - x):
        if i <= len(button_text) - 1:
            if selected == 0:
                screen_matrix[6][x + i] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[6][x + i] = button_text[i]

    button_text = ' Load '
    for i in range(tui_width - x):
        if i <= len(button_text)-1:
            if selected == 1:
                screen_matrix[6][x + i + 7] = formatTextAsSelected(button_text[i])
            else: 
                screen_matrix[6][x + i + 7] = button_text[i]
    
    button_text = ' New '
    for i in range(tui_width - x):
        if i <= len(button_text) - 1:
            if selected == 2:
                screen_matrix[7][x + i + 4] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[7][x + i + 4] = button_text[i]
    
    button_text = ' Clear '
    for i in range(tui_width - x):
        if i <= len(button_text) - 1:
            if selected == 3:
                screen_matrix[8][x + i + 3] = formatTextAsSelected(button_text[i])
            else:
                screen_matrix[8][x + i + 3] = button_text[i]
                
    return screen_matrix

# Draw info about selected instrument:
def draw_info_instrument(screen_matrix, selected_instrument):
    tui_width = 64
    x = 2 + 6*8
    text_line_1 = 'Inst. info:'
    for i in range(len(text_line_1)):
        screen_matrix[10][x + i + 1] = text_bg_color('blue', text_line_1[i])
    
    lines = []
    if selected_instrument == 'Drums':
        text_line_1 = ' Drums and'
        text_line_2 = '  Samples'
        lines = [text_line_1, text_line_2]
    elif selected_instrument == 'Empty':
        text_line_1 = '  [insert]'
        text_line_2 = 'to add midi'
        lines = [text_line_1, text_line_2]
        
    else:
        text_line_1 = 'Midi Port: ' + selected_instrument[1]
        text_line_2 = ' Channel: ' + selected_instrument[-1]
        if len(selected_instrument) == 5:
            text_line_2 = ' Channel ' + selected_instrument[-2:]
        lines = [text_line_1, text_line_2]
        

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            screen_matrix[11 + i][x + j + 1] = text_bg_color('blue', lines[i][j])

    
    return screen_matrix

def draw_patterns(screen_matrix, selected_pattern, playlist, first_number, pattern_cursor):
    if pattern_cursor is not None:
        pattern_cursor[1] = pattern_cursor[1] - 1
    
    x = 2
    for i in range(len(playlist)):
        for j in range(len(playlist[i])):
            if j < first_number + 16:
                if playlist[i][j] is not None:
                    playlist_element_to_print = ' ' + str(playlist[i][j])
                    pattern_number_length = len(str(playlist_element_to_print))
                    for k in range(pattern_number_length):
                        if pattern_cursor is not None and pattern_cursor[0] == i and pattern_cursor[1] % 16 == j:
                            screen_matrix[j+1][x+k] = formatTextAsSelected(str(playlist_element_to_print)[k])
                        elif j % 2 == 0:
                            screen_matrix[j+1][x+k] = text_bg_color('black grey', str(playlist_element_to_print)[k])
                        else:
                            screen_matrix[j+1][x+k] = str(playlist_element_to_print)[k]
        x += 6
    return screen_matrix

# Draw page of the instrument (as max 8 can be displayed on the screen, and there can be many more instrumnets applied), draw info about playing/pause
def draw_page_and_playing(screen_matrix, page_number, is_playing):
    x = 2 + 6*8
    text_to_print = 'Page: ' + str(page_number)
    
    for i in range(len(text_to_print)):
        screen_matrix[15][x + i + 3] = text_bg_color('blue', text_to_print[i])
    
    if is_playing:
        text_to_print = 'Playing'
        z = 3
    else:
        text_to_print = 'Pause'
        z = 4
    
    for i in range(len(text_to_print)):
        screen_matrix[16][x + i + z] = text_bg_color('blue', text_to_print[i])
    
    return screen_matrix

def draw_songname(screen_matrix, songname):
    if songname == 'No songname':
        songname = '  [Song not saved!]'
    
    tui_width = 64
    x = 2 + 6*8
    text_line_1 = 'Song name:'
    for i in range(len(text_line_1)):
        screen_matrix[10][x + i + 2] = text_bg_color('blue', text_line_1[i])
    
    lines = []
    if len(songname) > 24:
        lines.append(songname[:12])
        lines.append(songname[12:23] + '…')
    elif len(songname) > 12:
        lines.append(songname[:12])
        lines.append(songname[12:])
    elif len(songname) <= 12:
        lines.append(songname)

    for i in range(len(lines)):
        line_len = len(lines[i])
        centered = int((13 - line_len) / 2)
        for j in range(len(lines[i])):
            screen_matrix[11 + i][x + j + centered] = text_bg_color('blue', lines[i][j])
    return screen_matrix

def main(list_of_instruments, bpm_value, swing_value, vol_value, 
     playlist, menu_selected=None, tui_cursor=None, is_playing=False, 
     songname='DNB24421.btp', printtui=True
):
        
    page_number = int(tui_cursor[0]/8) + 1
    first_instrument_to_display = int(tui_cursor[0] / 8) * 8
    list_of_instruments_to_display = list_of_instruments[first_instrument_to_display: first_instrument_to_display+8]
    
    first_number = (int(tui_cursor[1] / 16) * 16) + 1
    if tui_cursor[1] % 16 == 0:
        first_number -= 16
    if tui_cursor[1] == 0:
        first_number = 1
    playlist_to_display = []

    for i in range(len(playlist)):
        playlist_to_display.append(playlist[i][first_number-1: first_number -1 + 16])
    playlist_to_display = playlist_to_display[first_instrument_to_display: first_instrument_to_display+8]
    
    
    if menu_selected is not None:
        tui_cursor = None
    
    if tui_cursor is not None:
        if tui_cursor[1] == 0:
            selected_pattern = tui_cursor[0] % 8
            pattern_cursor = None
        else:
            pattern_cursor = tui_cursor
            selected_pattern = None
    else:
        selected_pattern = None
        pattern_cursor = None
    
    screen_matrix = create_screen_matrix()
    screen_matrix = fill_matrix(screen_matrix)
    screen_matrix = draw_frames_and_numbers(first_number, screen_matrix=screen_matrix)
    screen_matrix = name_tracks(screen_matrix=screen_matrix, list_of_samples=list_of_instruments_to_display, selected=selected_pattern)
    screen_matrix = draw_info_mode(screen_matrix)
    screen_matrix = draw_menu(screen_matrix, selected=menu_selected)
    screen_matrix = draw_bpm_vol_swing_values(screen_matrix, bpm_value, swing_value, vol_value)
    if selected_pattern is not None:
        screen_matrix = draw_info_instrument(screen_matrix, list_of_instruments_to_display[selected_pattern])
    else:
        screen_matrix = draw_songname(screen_matrix, songname)
    screen_matrix = draw_vertical_lines(screen_matrix)
    screen_matrix = draw_patterns(screen_matrix, selected_pattern, playlist_to_display, first_number, pattern_cursor)
    screen_matrix = draw_page_and_playing(screen_matrix, page_number, is_playing)
    if printtui:
        print_screen_matrix(screen_matrix)
    else:
        return screen_matrix
    
if __name__ == '__main__':
    # Tests
    playlist = [[1, None, 2, None],[4000,400,32,134]]
    selected_pattern = [1, 2]
    main(list_of_instruments=['Drums', 'M1C1'], bpm_value=200, swing_value=50, vol_value=90, playlist=playlist, tui_cursor=[0, 3])
    #cursor [instrument, quareternote]
