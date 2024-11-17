from txtcolor import text_bg_color
from txtcolor import text_font_color

# Constans:
TUI_WIDTH = 64
TUI_HIGHT = 17

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
    move_cursor += move_down(y-1)
    move_back_cursor += move_down(TUI_HIGHT-y+1)
    if x > 0:
        move_cursor += move_right(x)
    print('\033[H', end='')
    print(move_cursor, end='', flush=True)
    print(text, end='', flush=True)
    print(move_back_cursor, end='\r', flush=True)

# Testing:
def test_frame():
    print('\033[48;5;93m')
    for i in range(16):
        n = 64 - len(str(i))-1
        print(i, ' '*n)
    print('16', ' '*60, "\033[0m", flush=True)

if __name__ == '__main__':
    test_frame()
    overprint(y=0, x=30, text='test', bg_color='green')
    while True: pass