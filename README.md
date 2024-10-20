# BuzzStation
Physical Music Tracker project for Pi Zero 2 and Arduino Nano with audio samples support and MIDI outputs.

Drum Machine and samples:
Tracker will support audio samples.
Creating drums and sample loops will be done with music tracker GUI.
Therer will be able to see 8 sample tracks on the screen at once, but it will be able to scroll the view sideways, making it possible to load and operate on more than 8 samples.

MIDI:
There would be a connection between Pi Zero and Arduino Nano via Serial USB in order to get 3 * UART, to which 3 Midi females will be connected so the BuzzStation. So the BuzzStation will be acting as sequencer for 3 Midi outputs.
Entering music notes will be done in piano roll.

Inputs:
User inputs will be carried out via 3x4 keypad and potentiometres.
To Pi Zero there will be 2 potentiometers (for BPM and Swing adjust) connected via ADC (connection between ADC and Pi via I2C).

Outputs:
GUI will be presented on 7inch LCD screen conected via HDMI. 
Sound from Tracker will be carried out via USB external music card.

Format:
Song projects will be saved in .btp format.

Song Struckture:
Loop - for example 16 notes, Each Loop can loop forever, playing 16 notes repetitively.
Playlist - Matrix with the help of which from loops will be able to arrange into a larger part of a musical piece.In this matrix, you will be able to set as many loops as you want, so that they play simultaneously (for example, one loop plays only kick, the second snare, the third melody sent by one of the MIDI outputs).

## Required Libraries

This project requires the following Python libraries:

- `adafruit-circuitpython-ads1x15`  # Adafruit CircuitPython library for ADS1x15 ADCs
- `pygame 2.1.2`  # Pymixer from pygame used for playing audio samples
