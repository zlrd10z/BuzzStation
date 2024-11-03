from libs.keypad import Keypad
import os
from tui.midi_params_menu import tui_pick_midi_instrument
from core.midi_params_menu.send_controllers_data import send_picked_instrument


def create_instruments_dic():
    midi_instruments = {}
    with open('core/midi_params_menu/midi_instruments_list.txt', 'r') as file:
        for line in file:
            line = line.split(chr(9))
            if line[1] not in midi_instruments:
                midi_instruments[line[1]] = {}
            midi_instruments[line[1]][line[2].replace('\n', '')] =  line[0]
    return midi_instruments

def menu_select_instrument(keys, midi_instruments, instrument_type, midi_output, currently_selected_midi_instrument):
    instruments = list(midi_instruments[instrument_type].keys())
    selected = 0
    tui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
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
            tui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                              currently_selected_midi_instrument, instrument_type
                             )

def menu_instrument_types(keys, midi_instruments, midi_output, currently_selected_midi_instrument):
    instrument_types = list(midi_instruments.keys())
    selected = 0
    result = None
    tui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                  currently_selected_midi_instrument
                 )
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
            tui_pick_midi_instrument.main(midi_instruments, midi_output, selected, 
                                          currently_selected_midi_instrument
                                         )
    
def main(keys, song_data, midi_output, currently_selected_midi_instrument):
    midi_instruments = create_instruments_dic()
    result = menu_instrument_types(keys, midi_instruments, midi_output, currently_selected_midi_instrument)
    if result is not None:
        instrument_midi_dec = result[1]
        send_picked_instrument(song_data, midi_output, instrument_midi_dec)
    return result
    
if __name__ == '__main__':
    # Tests
    keys = Keypad()
    result = main(keys, 'M1CH1', 'Acoustic Grand Piano')
    print(result)
