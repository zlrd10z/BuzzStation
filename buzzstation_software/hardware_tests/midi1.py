# This code is Python adaptation of C code for arduino from https://docs.arduino.cc/built-in-examples/communication/Midi/
import time
import serial


# UART configuration:
ser = serial.Serial(
    port='/dev/serial0',      # /dev/serial0 as UART for Pi Zero
    baudrate=31250,           # MIDI rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def note_on(cmd, pitch, velocity):
     # Send channel, pitch and velocity to MIDI output via UART:
    ser.write(bytes([cmd, pitch, velocity]))

try:
    while True:
        # Od F#-0 (0x1E) do F#-5 (0x5A)
        for note in range(0x1E, 0x5A):
            # Note On (0x90 = channel 1), Note, velocity 0x45
            note_on(0x90, note, 0x45)
            time.sleep(0.1)  # Czekamy 100 ms
            # Note Off (0x90 = channel 1), Note, velocity 0x00
            note_on(0x90, note, 0x00)
            time.sleep(0.1)  # wait 100 ms

except KeyboardInterrupt:
    #close serial after keyboard interrupt:
    ser.close()
