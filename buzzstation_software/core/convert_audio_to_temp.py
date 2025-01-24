from pydub import AudioSegment
import os
from decimal import Decimal


#transorm note to speed for pygame mixer
def note_to_speed(note_n_octave):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if ' ' in note_n_octave:
        note_n_octave = note_n_octave.replace(' ', '')
    note = note_n_octave[:-1]
    octave = int(note_n_octave[-1])
    # result of 2 / 11, differnce is speed of note vibration between two quarter notes:
    quarter_speed_diff = Decimal(1/12)
    #5 as default refernce octave:
    octave_diff = octave - 5
    n = notes.index(note)
    if octave_diff >= 0:
        octave_speed = pow(2, octave_diff)
        note_speed = Decimal(octave_speed) * (Decimal(n) * quarter_speed_diff + 1)
    else:
        octave_speed = Decimal(1 / pow(2, abs(octave_diff)))
        note_speed = Decimal(octave_speed) * (Decimal(n) * quarter_speed_diff + 1)
    
    return note_speed

def convert_to_pygame_format(input_path, note_n_octave='C5'):
    cwd = os.getcwd()
    filename = input_path.split('/')[-1] #get filename from path
    filename = filename.split('.')[0] #extract filename without extension
    filename += '_' + note_n_octave
    output_path = cwd + '/.temp/' + filename

    audio = AudioSegment.from_file(input_path)

    # Apply speed change
    if note_n_octave != 'C5':
        speed_factor = note_to_speed(note_n_octave)
        new_frame_rate = int(audio.frame_rate * speed_factor)
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})

    # Convert to pygame settings (44100 Hz, 16-bit, stereo)
    audio = audio.set_frame_rate(44100)  
    audio = audio.set_sample_width(2)  #16-bit
    audio = audio.set_channels(2)  #stereo

    #save as wav
    audio.export(output_path, format='wav')
    
    return filename
