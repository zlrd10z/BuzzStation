import serial
import time
import threading 

NOTE_OFF_BYTE = bytes([123, 0])

uart = serial.Serial(
    port='/dev/serial0',  
    baudrate=31250  
)

lock = threading.Lock()

def send_data(data):
    with lock:
        try:
            if not uart.is_open:
                uart.open()  
            uart.write(data)  

        except KeyboardInterrupt as exception:
            print(exception)                

        finally:
            uart.close()   

def all_notes_off():
    channel1_noteoff = 176
    for i in range(16):
        channel = channel1_noteoff + i
        channel = bytes([channel])
        send_data(channel + NOTE_OFF_BYTE)

# For hardware/software testing purpose:        
if __name__ == "__main__":
    #note C5 on:
    bytes_to_send_1 = ([144, 72, 50])
    
    #note C5 off:
    bytes_to_send_2 = ([144, 72, 0])
    
    while True:
        send_data(bytes_to_send_1)
        time.sleep(0.1)
        send_data(bytes_to_send_2)
        time.sleep(0.1)
