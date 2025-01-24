from tui.midi_params_menu import tui_midi_menu
from core.midi_params_menu import submenus
from . import pick_midi_instrument
import os

clear_screen = lambda: os.system('clear')

def plus_minus_keys(song_data, key, selected, track):
    midi_outputs = song_data.get_data('playlist_list_of_instruments')
    midi_out_chnl = midi_outputs[track]
    midi_output = int(midi_out_chnl[1])
    midi_channel = int(midi_out_chnl[3:])
    if selected == 0:
        if key == '7' or key == '4':
            if midi_output == 1:
                midi_output = 3
            else:
                midi_output -= 1
        if key == '9' or key == '6':
            if midi_output == 3:
                midi_output = 1
            else:
                midi_output += 1
    if selected == 1:
        if key == '7' or key == '4':
            if midi_channel == 1:
                midi_channel = 16
            else:
                midi_channel -= 1
        if key == '9' or key == '6':
            if midi_channel == 16:
                midi_channel = 1
            else: 
                midi_channel += 1
    midi_outputs[track] = 'M' + str(midi_output) + 'c' + str(midi_channel)
    song_data.put_data("playlist_list_of_instruments", midi_outputs)
    return midi_outputs[track]

def main(keypad, song_data, midi_out_chnl='M1c1', selected_midi_instrument=('Synth Pad 1', 44), track=1):
    menu_categories = ['MIDI output: ', 'MIDI channel: ' , 'MIDI Instrument: ', 'Sound Envelopes',]
    menu_categories = menu_categories + ['Filter', 'Chorus', 'Phaser', 'Reverb','Delay']
    selected_midi_instrument = selected_midi_instrument[0]
    selected = 0
    tui_midi_menu.main(midi_out_chnl, selected_midi_instrument, track, selected)

    # main loop:
    while True:
        key = keypad.check_keys()
        if key != '':
            # Direction keys:
            if key == '2' and selected - 1 >= 0:
                selected -= 1
            if key == '8' and selected + 1 < 9:
                selected += 1
            # [Esc] key - abort:
            if key == '1':
                break
            # [-] and [+] or [left arrow] and [right arrow] keys - toggle values:
            if key == '7' or key == '9' or key == '4' or key == '6': #[-]
                if selected < 2:
                    midi_out_chnl = plus_minus_keys(song_data, key, selected, track)
            # [Insert] key or [E] edit key - accept / proceed:
            if key == '5' or key == '3':
                if selected == 2:
                    midi_instruments = song_data.get_data('playlist_list_of_midi_assigned')
                    tmp_selected_midi_instrument = pick_midi_instrument.main(keypad, song_data, midi_out_chnl, selected_midi_instrument)
                    if tmp_selected_midi_instrument is not None:
                        midi_instruments[midi_out_chnl] = tmp_selected_midi_instrument
                        selected_midi_instrument = tmp_selected_midi_instrument[0]
                        song_data.put_data('playlist_list_of_midi_assigned', midi_instruments)
                elif selected > 2:
                    category = menu_categories[selected]
                    submenus.main(keypad, song_data, track, category, midi_out_chnl)
            tui_midi_menu.main(midi_out_chnl, selected_midi_instrument, track, selected)
