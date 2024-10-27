from tui.txtcolor import text_font_color, text_bg_color
from tui.scrmx import clear_screen
import sys
import os


x = 0
y = 0
save_x = 0
keyboard_matrix = []

def append_keyboard_matrix():
    keyboard_row1 = []
    keyboard_row2 = []
    keyboard_row3 = []
    keyboard_row4 = []
    keyboard_row5 = ['Backspace', 'Save']

    for i in range(9):
        keyboard_row1.append(str(i+1))
    keyboard_row1.append(str(0))
    keyboard_row1.append('_')

    r2 = 'qwertyuiop'
    r3 = 'asdfghjkl'
    r4 = 'zxcvbnm'

    for i in range(len(r2)):
        keyboard_row2.append(r2[i])
    for i in range(len(r3)):
        keyboard_row3.append(r3[i])
    for i in range(len(r4)):
        keyboard_row4.append(r4[i])

    keyboard_matrix.append(keyboard_row1)
    keyboard_matrix.append(keyboard_row2)
    keyboard_matrix.append(keyboard_row3)
    keyboard_matrix.append(keyboard_row4)
    keyboard_matrix.append(keyboard_row5)

append_keyboard_matrix()

def change_cursor_position(direction):
    global x
    global y
    global save_x
    if direction == 'up':
        old_y = y
        if y == 0:
            y = len(keyboard_matrix) - 1
        else:
            y -= 1
        if old_y == 4:
            x = save_x
        elif x > len(keyboard_matrix[y]) - 1:
            x = len(keyboard_matrix[y]) - 1
    if direction == 'down':
        old_y = y
        # Curson jump from last row to first row:
        if y == (len(keyboard_matrix)-1):
            y = 0
            # last row has two wide buttons: [backspace] and [save]. If it's jumps from [save] to first row, it jumps to button [5], 
            # so it will be visualy predictible, where cursor will land:
            if x == 1: x = 4 
        # Change row one level down:
        else:
            y += 1
        # if cursor is first row on top of last row with wide buttons, when in jump to last row, it jumps on aprpoiate wide button,
        # which is right under the button from which cursor is jumping
        if y == 4:
            save_x = x
            if int(len(keyboard_matrix[old_y])/2) > x:
                x = 0
            else: x = 1
        #if cursors is on the last button in row, and the row is wider that next row, where cursor is jumping, it took last button in the next row: 
        elif x > len(keyboard_matrix[y]) - 1:
            x = len(keyboard_matrix[y]) - 1    
    if direction == 'left':
        if x == 0:
            x = (len(keyboard_matrix[y]) - 1)
        else:
            x -= 1
    if direction == 'right':
        if x == (len(keyboard_matrix[y]) - 1):
            x = 0
        else:
            x += 1

fill = text_font_color('purple', '█')

def print_keyboard(filename, is_dir):
    def print_colored_line(text):
        number_of_fields_to_fill = 64 - len(text)
        text += ' ' * number_of_fields_to_fill
        text = text_bg_color('blue', text)
        print(text)
    clear_screen()
    print_colored_line('  Please enter the name of song project')
    # starting index to print keyboard on center of the screen, between each key there would be two spaces
    # screen width 64 signs - 2 chars for bottom and top blue line, divided by two to get ceneter
    keyboard_print_index_start_width = int((64 - 2 - (len(keyboard_matrix[0]*3)) - 3) / 2)
    keyboard_print_index_start_height = int((17 - 2 - len(keyboard_matrix)) / 2) + 4
    for i in range(6):
        if i == keyboard_print_index_start_height-4:
            for j in range(5):
                text = fill + fill * keyboard_print_index_start_width
                for k in range(len(keyboard_matrix[j])):
                    if y == j and x == k:
                        text += (text_bg_color('grey', keyboard_matrix[j][k]))
                    else:
                        text += keyboard_matrix[j][k]
                    text += fill*2
                match j:
                    case 0:
                        text += fill*3
                    case 1:
                        text += fill*6
                    case 2:
                        text += fill*9
                    case 3:
                        text += fill*15
                    case 4:
                        text += fill*19

                text += fill * keyboard_print_index_start_width + (text_bg_color('blue', ' '))
                print(text)
                print((text_bg_color('blue', ' ')) + fill * 62 + (text_bg_color('blue', ' ')))
        # Print text, to emphasis that user create directory/file:
        elif i == keyboard_print_index_start_height - 8:
            center_text_index = int((64 - 2 - len('filename:')) / 2)
            if is_dir: 
                info = 'dir name:'
            else: 
                info = 'filename:'
            text = fill + ' ' * center_text_index + info + ' ' * center_text_index + ' ' + fill
            print(text)
        elif i == keyboard_print_index_start_height - 7:
            center_text_index = int((62 - len(filename)) / 2)
            text =  ' ' * center_text_index + filename + ' ' * center_text_index
            #text =  ' ' * center_text_index + str(y) + str(x) + ' ' * center_text_index
            if len(text) == 62:
                text = fill + text + fill
            else: 
                text = fill + text + ' ' + fill
            print(text)
        
        else:
            text = (text_bg_color('blue', ' ')) + fill * 62 + (text_bg_color('blue', ' '))
            print(text)

    print_colored_line(' Press [*] to abort.')
    
def user_input_filename(is_dir, keypad):
    filename = ''            
    k = keypad
    print_keyboard('', is_dir)
    while True:
        pressed_key = k.check_keys()
        if pressed_key != '':
            if pressed_key == '2': 
                change_cursor_position('up')
            elif pressed_key == '8': 
                change_cursor_position('down')
            elif pressed_key == '4': 
                change_cursor_position('left')
            elif pressed_key == '6': 
                change_cursor_position('right')
            # [Esc] key:
            elif pressed_key == '*':
                filename = ''
                break
            # Accept key:
            elif pressed_key == '5':
                row = y
                column = x
                if keyboard_matrix[row][column] == 'Backspace':
                    filename = filename[:-1]
                elif keyboard_matrix[row][column] == 'Save':
                    if is_dir == False:
                        filename += '.btp'
                    break
                else:
                    filename += keyboard_matrix[row][column]    

            print_keyboard(filename, is_dir)

    return filename
