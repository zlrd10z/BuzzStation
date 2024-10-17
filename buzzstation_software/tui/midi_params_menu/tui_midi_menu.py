from tui.scrmx import create_screen_matrix
from tui.scrmx import fill_matrix
from tui.scrmx import print_screen_matrix
from tui.txtcolor import text_bg_color
from tui.txtcolor import text_font_color

GUI_HEIGHT = 17
GUI_WIDTH = 64

chg_bgd_clr = lambda text: text_bg_color('blue', text)
# Format displayed text, so it looks like selected by cursor:
txt_color_sel = lambda text: text_bg_color('white', text_font_color('black', text)) 

# Fill screen with blue color:
def bg_color(screen_matrix):
    for y in range(len(screen_matrix)):
        for x in range(len(screen_matrix[y])):
            screen_matrix[y][x] = chg_bgd_clr(' ') 
    return screen_matrix

# Draw window title and separate it from the rest of data:
def draw_win_title(screen_matrix, track):
    for i in range(GUI_HEIGHT-1):
        screen_matrix[i][0] = screen_matrix[i][len(screen_matrix[1])-1] = chg_bgd_clr('┃')
    for x in range(len(screen_matrix[1])):
        screen_matrix[0][x] =  chg_bgd_clr('━')
        screen_matrix[2][x] =  chg_bgd_clr('━')
        screen_matrix[GUI_HEIGHT-2][x] =  chg_bgd_clr('━')
    screen_matrix[0][0] = chg_bgd_clr('┏')
    screen_matrix[0][len(screen_matrix[1])-1] = chg_bgd_clr('┓')
    screen_matrix[1][0] = screen_matrix[1][len(screen_matrix[1])-1] = chg_bgd_clr('┃')
    screen_matrix[2][0] = chg_bgd_clr('┣')
    screen_matrix[2][len(screen_matrix[1])-1] = chg_bgd_clr('┫')
    screen_matrix[GUI_HEIGHT-2][0] = chg_bgd_clr('┗')
    screen_matrix[GUI_HEIGHT-2][len(screen_matrix[1])-1] = chg_bgd_clr('┛')

    # Draw centered text:
    title_txt = 'Edit MIDI parametres for track ' + str(track) + ':'
    start_print_x = (GUI_WIDTH - len(title_txt))/2
    start_print_x = int(start_print_x)
    for i in range(len(title_txt)):
        screen_matrix[1][start_print_x+i] = chg_bgd_clr(title_txt[i])
    return screen_matrix

def draw_options(screen_matrix, midi_out_chnl, selected_midi_instrument, selected):
    addition_text = [midi_out_chnl[1], midi_out_chnl[3:], selected_midi_instrument]
    for i in range(3):
        if len(addition_text[i]) == 1:
            n = 1
        else:
            n = 0
        addition_text[i] = addition_text[i] + ' '*n

    texts = ['MIDI output: ', 'MIDI channel: ' , 'MIDI Instrument: ', 'Sound Envelopes',]
    texts = texts + ['Filter', 'Chorus', 'Phaser', 'Reverb', 'Delay']
    for i in range(len(texts)):
        if i < 3:
            for j in range(len(texts[i])):
                screen_matrix[3+i][1+j] = chg_bgd_clr(texts[i][j])
            for j in range(len(addition_text[i])):
                if i == selected:
                    # Format displayed text, so it looks like selected by cursor:
                    screen_matrix[3+i][18+j] = txt_color_sel(addition_text[i][j])
                else:
                    screen_matrix[3+i][18+j] = addition_text[i][j]
        else:
            for j in range(len(texts[i])):
                if i == selected:
                    screen_matrix[3+i][1+j] = txt_color_sel(texts[i][j])
                else:
                    screen_matrix[3+i][1+j] = chg_bgd_clr(texts[i][j])
    return screen_matrix

def draw_instruction(screen_matrix, selected):
    if selected < 2:
        text_instr = 'Press [-] or [+] to toggle MIDI '
        if selected == 0:
            text_instr += 'outputs.'
        if selected == 1:
            text_instr += 'channels.'
    else:
        text_instr = 'Press [Enter] to modify.'

    for i in range(len(text_instr)):
        screen_matrix[GUI_HEIGHT-1][1+i] = chg_bgd_clr(text_instr[i])

    return screen_matrix

def main(midi_out_chnl, selected_midi_instrument, track, selected):
    screen_matrix = create_screen_matrix()
    screen_matrix = fill_matrix(screen_matrix)
    screen_matrix = bg_color(screen_matrix)
    screen_matrix = draw_win_title(screen_matrix, track)
    screen_matrix = draw_options(screen_matrix, midi_out_chnl, selected_midi_instrument, selected)
    screen_matrix = draw_instruction(screen_matrix, selected)
    print_screen_matrix(screen_matrix)

if __name__ == '__main__':
    # Test
    main(midi_out_chnl='M1c16', selected_midi_instrument='Acoustic Grand Piano', track=1, selected=2)



#midi:
#title_txt = 'Edit parameters of MIDI output: ' + midi_out_chnl[1] + ', Channel: ' + midi_out_chnl[3:]
