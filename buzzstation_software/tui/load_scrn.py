from tui import scrmx
from tui.txtcolor import text_bg_color
from tui.txtcolor import text_font_color
import os


ascii_txt_loading = []
empty_line = ' ' * 48
ascii_txt_loading.append('  _     ___    _    ____ ___ _   _  ____        ')
ascii_txt_loading.append(' | |   / _ \  / \  |  _ \_ _| \ | |/ ___|       ')
ascii_txt_loading.append(' | |  | | | |/ _ \ | | | | ||  \| | |  _        ')
ascii_txt_loading.append(' | |__| |_| / ___ \| |_| | || |\  | |_| |_ _ _  ')
ascii_txt_loading.append(' |_____\___/_/   \_\____/___|_| \_|\____(_|_|_) ')
ascii_txt_loading.append(empty_line)

def draw_ascii_art(screen_matrix, x_start, y_start):
    for y in range(len(ascii_txt_loading)):
        for x in range(len(ascii_txt_loading[y])):
            screen_matrix[y+y_start][x+x_start] = ascii_txt_loading[y][x]

def draw():
    screen_matrix = scrmx.create_screen_matrix()
    scrmx.fill_matrix(screen_matrix)
    scrmx.bg_color(screen_matrix)
    scrmx.draw_box(screen_matrix)
    scrmx.draw_instr(screen_matrix, 'BuzzStation')
    draw_ascii_art(screen_matrix, 8, 6)
    #os.system('clear') #clear screen
    scrmx.print_screen_matrix(screen_matrix) #display loading screen

if __name__ == '__main__':
    draw()
