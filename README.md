# BuzzStation
Physical Music Tracker project for Pi Zero 2 and Arduino Nano with audio samples support and MIDI outputs.

current version: 1.0.0

## Drum Machine and samples:
Tracker supports audio samples.
Creating drums and sample loops can be done with music tracker TUI.

## MIDI:
There's a connection between Pi Zero and Arduino Nano via Serial USB in order to get 3 * UART, to which 3 MIDI females are connected so the BuzzStation. So the BuzzStation is acting as sequencer for 3 MIDI outputs.
Entering music notes will be done in piano roll.

## Inputs:
User inputs are carried out via 3x4 keypad and potentiometres.
To Pi Zero there will be 3 potentiometers (for BPM, Swing, and audio sampler volume adjust) connected via ADC (connection between ADC and Pi via I2C).

## Outputs:
TUI is presented on 7inch LCD screen conected via HDMI. 
Sound from Tracker is carried out via USB external music card.

## Format:
Song projects can be saved in .btp format with pickle.

## Song Struckture:
Loop - for example 16 notes, Each Loop can loop forever, playing 16 notes repetitively.
Playlist - Matrix with the help of which from loops will be able to arrange into a larger part of a musical piece.In this matrix, you will be able to set as many loops as you want, so that they play simultaneously (for example, one loop plays only kick, the second snare, the third melody sent by one of the MIDI outputs).

More information you can find in 'User Guide.docx'

## Required Libraries

This project requires the following Python libraries:

- `adafruit-circuitpython-ads1x15`  # Adafruit CircuitPython library for ADS1x15 ADCs
- `pygame 2.1.2`  # Pymixer from pygame used for playing audio samples
- `pydub 0.24.1` # pydub for audio converting

## Note:
This code is designed to run on Rasbian Lite with Kmscon for proper display of all Unicode characters.
