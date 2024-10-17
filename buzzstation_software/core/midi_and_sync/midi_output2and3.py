import serial
import time


serialUSB = serial.Serial('/dev/ttyUSB0', 31250) 
time.sleep(3)  # Wait for the connection:

stop_byte = 244
byte_midi_output_2 = 245
byte_midi_output_3 = 246
byte_all_notes_off = 247

# Note on: 144 - channel 1; 72 - note C5; 100 - volume 
# byte_note_c5 = bytes([144, 72, 50])

def send_data_to_arduino(data, output=None):
    try:
        if output == 2:
            data = byte_midi_output_2 + data
        if output == 3:
            data = byte_midi_output_3 + data
        data.append(stop_byte)
        data = bytes(data)        
        # Sending data to arduino:
        serialUSB.write(data)      
    except Exception as exception:
        print(exception)
        serialUSB.close()

def arduino_turnoff_all_notes():
    send_data_to_arduino(bytes([byte_all_notes_off]))
    
# For hardware/software testing purpose:
if __name__ == "__main__":

    # 245 - midi output 2; 246 - midi output 3; 144 - channel 1; 72 - note C5; 100 - volume:
    note_on_midi_output_2 = [245, 144, 72, 50]
    note_on_midi_output_3 = [246, 144, 72, 50]
    
    note_off_midi_output_2 = [245, 144, 72, 50]
    note_off_midi_output_3 = [246, 144, 72, 50]

    while True:
        send_data_to_arduino(note_on_midi_output_2 + note_on_midi_output_3)
        time.sleep(0.1)
        send_data_to_arduino(note_off_midi_output_2 + note_off_midi_output_3)
        time.sleep(0.1)
