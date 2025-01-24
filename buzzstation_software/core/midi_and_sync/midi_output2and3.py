import serial
import time
import threading


stop_byte = bytes([244])
byte_midi_output_2 = bytes([245])
byte_midi_output_3 = bytes([246])
byte_all_notes_off = bytes([247])

# Note on: 144 - channel 1; 72 - note C5; 100 - volume 
# byte_note_c5 = bytes([144, 72, 50])
lock = threading.Lock()

def send_data_to_arduino(serial_usb, data, output=None):
    with lock:
        try:
            if output == 2:
                data = byte_midi_output_2 + data
            if output == 3:
                data = byte_midi_output_3 + data
            data += stop_byte        
            # Sending data to arduino:
            serial_usb.write(data)

        except Exception as exception:
            print(exception)


