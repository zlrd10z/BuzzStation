import serial
import time


uart = serial.Serial(
    port='/dev/serial0',  
    baudrate=31250  
)

def send_data(data):
	try:
		if not uart.is_open:
			uart.open()  
			uart.write(data)  

	except KeyboardInterrupt as exception:
		print(exception)                

	finally:
		uart.close()   

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
