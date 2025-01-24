from libs.keypad import Keypad
from tui.midi_params_menu import sliders
from tui import scrmx
from core.song_data import SongData
from core.midi_params_menu.send_controllers_data import send_single_contrl_param
import os

'''
TEMPORARY TEST FUNCTIONS
'''
#clear_screen = lambda: os.system('clear')

def tui_sliders(title, slider_selected, instruction, percents):
    title += ':'
    screen_matrix = scrmx.create_screen_matrix()
    scrmx.fill_matrix(screen_matrix)
    scrmx.bg_color(screen_matrix)
    scrmx.draw_box(screen_matrix)
    scrmx.draw_title(screen_matrix, title)
    if isinstance(instruction, str):
        scrmx.draw_instr(screen_matrix, instruction)
    sliders.draw_sliders(screen_matrix,
                         slider_selected,
                         percents
                        )
    scrmx.print_screen_matrix(screen_matrix)

def plus_minus_keys(key, slider_sensitivity_10, param_val):
    if not slider_sensitivity_10:
        if key == '7' and param_val > 0:
            param_val -= 1
        elif key == '9' and param_val < 100:
            param_val   += 1
    else:
        if key == '7':
            if param_val-10 > 0:
                param_val -= 10
            else:
                param_val = 0
        elif key == '9':
            if param_val+10 < 100: 
                param_val += 10
            else:
                param_val = 100
    return param_val

def left_right_keys(prev_len, subcategory_params):
    if prev_len == 4:
        first_four_params = list(subcategory_params.items())[-2:]
        subcategory_params = dict(first_four_params)
    if prev_len == 2:
        first_four_params = list(subcategory_params.items())[:4]
        subcategory_params = dict(first_four_params)
    return subcategory_params

def main(keypad, song_data, track, title, midi_output_channel):
    subcategory_params = song_data.midi_misc_settings_operations(option='get', track=track, target_title=title)
    dict_keys = [*subcategory_params]
    sliders_number = len(subcategory_params)
    slider_selected = 0
    slider_sensitivity_10 = False
    
    if title == 'Filter':
        instruction = '[←][→]: toggle filter\'s parametres.'
        #6 sliders will not fit on the sceen, so divide them:
        first_four_params = list(subcategory_params.items())[:4]
        subcategory_params = dict(first_four_params)
        sliders_number = len(subcategory_params)
    else:
        instruction = 'Press [Insert] to increase slider movement'

    #clear_screen()
    tui_sliders(title, slider_selected, instruction, subcategory_params)

    # Main loop:
    while True:
        key = keypad.check_keys()
        if key != '':
            # Direction keys:
            if key == '2': #UP
                print(slider_selected)
                if slider_selected > 0:
                    slider_selected -= 1
                else:
                    slider_selected = sliders_number-1
                print(slider_selected)
            if key == '8': #DOWN
                if slider_selected < sliders_number-1:
                    slider_selected += 1
                else:
                    slider_selected = 0
            if key == '4' or key == '6': #Left and Right keys
                if title == 'Filter':
                    prev_len = len(subcategory_params)
                    subcategory_params = song_data.midi_misc_settings_operations(option='get', track=track, target_title=title)
                    subcategory_params = left_right_keys(prev_len, subcategory_params)
                    dict_keys = [*subcategory_params]
                    sliders_number = len(subcategory_params)
                    slider_selected = 0
            #[insert] key - change sensitivity of slider:
            if key == '5':
                if slider_sensitivity_10:
                    slider_sensitivity_10 = False
                    if title != 'Filter':
                        instruction = 'Press [Insert] to increase slider movement'
                else:
                    slider_sensitivity_10 = True
                    if title != 'Filter':
                        instruction = 'Press [Insert] to decrease slider movement'
            # [-] and [+] key - slide the slider
            if key == '7' or key == '9':
                param = dict_keys[slider_selected]
                param_val = subcategory_params[param]
                param_val = plus_minus_keys(key, slider_sensitivity_10, param_val)
                subcategory_params[param] = param_val
                params_to_update = song_data.midi_misc_settings_operations(option='get', track=track, target_title=title)
                params_to_update.update(subcategory_params)
                song_data.midi_misc_settings_operations(option='update', track=track, target_title=title, new_value=params_to_update)
                send_single_contrl_param(song_data, title, param, param_val, midi_output_channel)
            #[Esc] key - quit:
            if key == '1':
                break
            # Update screen:
            #clear_screen()
            tui_sliders(title, slider_selected, instruction, subcategory_params)

if __name__ == '__main__':
    keypad = Keypad()
    song_data = SongData()
    main(keypad, song_data, 1, 'Filter')
