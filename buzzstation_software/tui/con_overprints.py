from txtcolor import text_bg_color
from txtcolor import text_font_color

# Constants:
TUI_WIDTH = 64
TUI_HIGHT = 17
MOVE_LINE_BEG = '\r'

# Lambdas:
move_up = lambda n: '\033[F'*n
move_down = lambda n: f'\x1b[{n}B'
move_right = lambda n: '\033[C'*n

def overprint(y, x, text, bg_color=None, font_color=None):
    # Exceptions:
    class ScreenSizeValueError(Exception):
        pass
    if len(text) > TUI_WIDTH - x:
        raise ScreenSizeValueError(f"Text is longer than line!\nText size: {len(text)}")
    elif y < 0 or x < 0:
        raise ScreenSizeValueError(f"x and y cannot be smaller then 0.")
    # Operations:
    move_cursor = ''
    move_back_cursor = ''
    if bg_color is not None:
        text = text_bg_color(bg_color, text)
    if font_color is not None:
        text = text_font_color(font_color, text)

    # y is provided as coordinate, where y = 0 is first line from top
    y_prod = TUI_HIGHT-1-y
    if y_prod > 0:
        move_cursor += move_up(y_prod)
        move_back_cursor += move_down(y_prod)
    if x > 0:
        move_cursor += move_right(x)
        move_back_cursor += MOVE_LINE_BEG
    print(move_cursor, end='', flush=True)
    print(text)
    print(move_back_cursor, end='', flush=True)

# Testing:

def test_frame():
    print('\033[48;5;93m', end='')
    for i in range(16):
        print(''*64)
    print(''*64, end='', flush=True)
    print("\033[0m")

if __name__ == '__main__':
    test_frame()
    overprint(y=1, x=1, text='test', bg_color='green')
    #while True: pass