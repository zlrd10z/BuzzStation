import serial
import time


stop_byte = 244
byte_midi_output_2 = 245
byte_midi_output_3 = 246
byte_all_notes_off = 247

# Note on: 144 - channel 1; 72 - note C5; 100 - volume 
# byte_note_c5 = bytes([144, 72, 50])

def send_data_to_arduino(data, serial_usb, output=None):
    try:
        if output == 2:
            data = byte_midi_output_2 + data
        if output == 3:
            data = byte_midi_output_3 + data
        data.append(stop_byte)
        data = bytes(data)        
        # Sending data to arduino:
        serial_usb.write(data)      
    except Exception as exception:
        print(exception)

git commit -m "Added: sending midi controlers singals via midi outputs, midi_output2and3 is now getting serial from songa data'
