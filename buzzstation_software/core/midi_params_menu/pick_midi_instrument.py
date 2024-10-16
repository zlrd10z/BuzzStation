from libs.keypad import Keypad
import os
from gui.midi_params_menu import gui_pick_midi_instrument


clear_screen = lambda: os.system('clear')

def menu_select_instrument(keys, midi_instruments, instrument_type, midi_output, currently_selected_midi_instrument):
    instruments = list(midi_instruments[instrument_type].keys())
    selected = 0
    gui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                                  currently_selected_midi_instrument, instrument_type
                                 )
    while True:
        key = keys.check_keys()
        if key != '':
            # Down key:
            if key == '2' and selected > 0:
                selected -= 1
            # Up key:
            if key == '8' and selected < len(instruments) - 1:
                selected += 1
            # Accept key:
            if key == '5':
                result = (instruments[selected], int(midi_instruments[instrument_type][instruments[selected]]))
                return result
            # Esc Key:
            if key == '1':
                break
            # Update GUI:
            gui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                              currently_selected_midi_instrument, instrument_type
                             )

def menu_instrument_types(keys, midi_instruments, midi_output, currently_selected_midi_instrument):
    instrument_types = list(midi_instruments.keys())
    selected = 0
    result = None
    gui(midi_instruments, midi_output, selected, currently_selected_midi_instrument)
    while True:
        key = keys.check_keys()
        if key != '':
            # Down key:
            if key == '2' and selected > 0:
                selected -= 1
            # Up key:
            if key == '8' and selected < len(instrument_types) - 1:
                selected += 1
            # Accept key:
            if key == '5':
                result = menu_select_instrument(keys, midi_instruments, instrument_types[selected], midi_output, currently_selected_midi_instrument)
                if result is not None:
                    return result
            # Esc Key:
            if key == '1':
                break
                gui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                                  currently_selected_midi_instrument
                                 )
    
def main(keys, midi_output, currently_selected_midi_instrument):
    midi_instruments = create_instruments_dic()
    result = menu_instrument_types(keys, midi_instruments, midi_output, currently_selected_midi_instrument)
    return result
    
if __name__ == '__main__':
    # Tests
    keys = Keypad()
    result = main(keys, 'M1CH1', 'Acoustic Grand Piano')
    print(result)
