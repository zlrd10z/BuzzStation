from gui import gui_warning_window
from gui.gui_tracker import create_screen_matrix
from gui.gui_tracker import fill_matrix
from libs.keypad import Keypad
import os


def main(keypad, screen_matrix, action):
    clear_screen = lambda: os.system('clear')
    ok_selected = False

    clear_screen()
    gui_warning_window.main(screen_matrix, ok_selected, action)

    while True:
        key = keypad.check_keys()
        if key != '':
            # Direction key - left:
            if key == '4' and not ok_selected:
                ok_selected = True
            # Direction key - right:
            if key == '6' and ok_selected:
                ok_selected = False
            # [Insert] key - accept:
            if key == '5':
                result = ok_selected
                break
            # [Esc] key - abort:
            if key == '1':
                result = False
                break
            clear_screen()
            gui_warning_window.main(screen_matrix, ok_selected, action)
    return result

if __name__ == '__main__':
    # Test
    screen_matrix = create_screen_matrix()
    screen_matrix = fill_matrix(screen_matrix)
    keypad = Keypad()
    action = 'new song'
    result = main(keypad, screen_matrix, action)
    print(result)