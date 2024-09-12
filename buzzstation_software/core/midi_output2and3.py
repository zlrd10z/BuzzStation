import serial
import time


serialUSB = serial.Serial('/dev/ttyUSB0', 31250) 
time.sleep(3)  # Wait for the connection:

stop_byte = 221
byte_midi_output_2 = 222
byte_midi_output_3 = 223

# 1 - channel 1; 72 - note C5; 100 - volume 
byte_note_c5 = bytes([144, 72, 50])
volume0 = bytes([0])



def sendDataToArduino(data):
	try:
		data.append(stop_byte)
		data = bytes(data)		
		
		# Sending data to arduino:
		serialUSB.write(data)  	

	except KeyboardInterrupt as exception:
		print(exception)
		serialUSB.close()

		

def turnOffAllNotesOnArduino():
	data = []
	for i in range(2):
		for j in range(len(16)):
			if i == 0:
				data.append(223)
			else:
				data.append(224)
			
			data.append(176 + j) #channel control
			data.append(123) #all notes off 
			data.append(0) #has to be 0
	
	sendDataToArduino(data)
	
	
# For hardware/software testing purpose:
if __name__ == "__main__":
	byte_midi_output_2 = bytes([222])
	byte_midi_output_3 = bytes([223])

	# 222 - midi output 2; 223 - midi output 3; 144 - channel 1; 72 - note C5; 100 - volume:
	note_on_midi_output_2 = [222, 144, 72, 50]
	note_on_midi_output_3 = [223, 144, 72, 50]
	
	note_off_midi_output_2 = [222, 144, 72, 50]
	note_off_midi_output_3 = [223, 144, 72, 50]

	while True:
		sendDataToArduino(note_on_midi_output_2 + note_on_midi_output_3)
		time.sleep(0.1)
		sendDataToArduino(note_off_midi_output_2 + note_off_midi_output_3)
		time.sleep(0.1)
