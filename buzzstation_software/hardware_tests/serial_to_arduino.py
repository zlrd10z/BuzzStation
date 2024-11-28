import serial
import time


serialUSB = serial.Serial('/dev/ttyUSB0', 31250) 
time.sleep(2)  # Wait for connection

stop_byte = bytes([221])
byte_midi_output_2 = bytes([222])
byte_midi_output_3 = bytes([223])

# 1 - channel 1; 72 - note C5; 100 - volume 
byte_note_c5 = bytes([144, 72, 50])
volume0 = bytes([0])

bytes_to_send = [byte_midi_output_3[0], byte_note_c5[0], byte_note_c5[1], byte_note_c5[2], stop_byte[0]]
bytes_to_send2 = [byte_midi_output_3[0], byte_note_c5[0], byte_note_c5[1], volume0[0], stop_byte[0]]

try:
    while True:
        # Wysyłanie komendy do Arduino
        serialUSB.write(bytes_to_send)  # Wysyła komendę '1' do Arduino
        print(bytes_to_send2)
        
        if serialUSB.in_waiting > 0:  # Sprawdza, czy są dostępne dane do odczytu
            data = serialUSB.read(serialUSB.in_waiting)  # Odczytuje wszystkie dostępne dane
            print(data)
        
        time.sleep(0.1)  # Czekaj 1 sekundę
        serialUSB.write(bytes_to_send2) 
        time.sleep(0.1)

except KeyboardInterrupt:
    serialUSB.close()
