from core.song_data import SongData
from core.midi_and_sync import midi_output1
print('x')
from core.midi_and_sync import midi_output2and3
print('y')
CHANNEL_CHG = 175 #176 for channel 1 and so on up to channel 16
BYTE_MIDI_OUT_2 = bytes([245])
BYTE_MIDI_OUT_2 = bytes([246])

#Controlers and it's bytes:
#param_collection     #param_category     #param: param_byte
cc_second_byte = {'Sound Envelopes' : {'Attack' : 73, 
                                       'Delay' : 75, 
                                       'Sustain' : 70, 
                                       'Release' : 72
                                      },
                  'Filter' : {'Attack' : 79, 
                              'Delay' : 80, 
                              'Sustain' : 81, 
                              'Release' : 82,
                              'Cutoff' : 74,
                              'Resonance' : 71,
                              },
                  'Chorus' : {'Level' : 93, 
                              'Rate' : 76, 
                              'Depth' : 77, 
                              'Feedback' : 78
                             },
                  'Phaser' : {'Depth' : 95, 
                              'Rate' : 92, 
                              'Feedback' : 93, 
                             }, 
                  'Reverb' : {'Level' : 91, 
                              'Time' : 83, 
                              'Pre-Delay' : 84, 
                             }, 
                  'Delay' : {'Level' : 94, 
                             'Time' : 82, 
                             'Feedback' : 81,
                            } 
                 }

'''
This function sends all contorller data, like for filters and reverb via MIDI outputs
'''

#scale numbers from 0-100 range to 0-127:
scale_percents_to_byte = lambda x: bytes([int((127 / 100) * x)])

def main(song_data, selected_output_channel=None):
    params_collection = song_data.get_data('midi_misc_settings')
    midi_outputs = [*params_collection]
    ins = song_data.get_data('playlist_list_of_instruments')

    # for each channel and midi output: 
    for i in range(len(midi_outputs)):
        # send only to selected output and channel:
        if selected_output_channel is not None:
            if selected_output_channel != selected_output_channel:
                continue

        # send only to channels in use:
        midi_output_channel = midi_outputs[i]
        if midi_output_channel in ins:
            midi_output = midi_output_channel[1]
            midi_channel = int(midi_output_channel[3:])
            cc_byte = bytes([CHANNEL_CHG + midi_channel])
            data_to_send = bytes([])

            # Prepare data to send for all parametres for single channel for selected midi output:
            for (_, cat_num), (_, cat_val) in zip(cc_second_byte.items(), params_collection[midi_output_channel].items()):
                for (_,controller_num), (_, controller_val) in zip(cat_num.items(), cat_val.items()):
                    # Bytes informing arduino, to which midi output it should push the data:
                    if midi_output_channel[1] == '2':
                        data_to_send += BYTE_MIDI_OUT_2
                    elif midi_output_channel[1] == '3':
                        data_to_send += BYTE_MIDI_OUT_3
                    param_byte = bytes([controller_num])
                    value_byte = scale_percents_to_byte(controller_val)
                    data_to_send = data_to_send + cc_byte + param_byte + value_byte

            # Send data to selected output:
            if midi_output_channel[1] == '1':
                midi_output1.send_data(data_to_send)
            else:
                midi_output2and3.send_data_to_arduino(data_to_send)

if __name__ == '__main__':
    # Tests
    song_data = SongData()
    ins = song_data.get_data('playlist_list_of_instruments')
    ins[1] = 'M1c1'
    song_data.put_data('playlist_list_of_instruments', ins)
    new_value = {'Attack' : 100, 
               'Delay' : 80, 
               'Sustain' : 30, 
               'Release' : 14
              }
    song_data.midi_misc_settings_operations('update', 1, new_value, 'Sound Envelopes')
    main(song_data)