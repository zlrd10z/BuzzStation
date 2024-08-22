import time
import serial

# Konfiguracja portu UART (na Raspberry Pi Zero to /dev/serial0)
ser = serial.Serial(
    port='/dev/serial0',      # Używamy /dev/serial0 dla UART
    baudrate=31250,           # Typowa prędkość transmisji MIDI
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def note_on(cmd, pitch, velocity):
    """
    Wysyła komunikat MIDI Note On lub Note Off przez UART.
    """
    ser.write(bytes([cmd, pitch, velocity]))

try:
    while True:
        # Od F#-0 (0x1E) do F#-5 (0x5A)
        for note in range(0x1E, 0x5A):
            # Note On (0x90 = kanał 1), nuta, velocity 0x45
            note_on(0x90, note, 0x45)
            time.sleep(0.1)  # Czekamy 100 ms
            # Note Off (0x90 = kanał 1), nuta, velocity 0x00
            note_on(0x90, note, 0x00)
            time.sleep(0.1)  # Czekamy 100 ms

except KeyboardInterrupt:
    # Zamykanie połączenia serial przy zakończeniu programu
    ser.close()
