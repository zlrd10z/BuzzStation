from pydub import AudioSegment
import os


def convert_to_pygame_format(input_path):
    cwd = os.getcwd()
    filename = input_path.split('/')[-1] #get filename from path
    filename = filename.split('.')[0] #extract filename without extension
    output_path = cwd + '/.temp/' + filename + ".wav"

    audio = AudioSegment.from_file(input_path)
    
    # Convert to pygame settings (44100 Hz, 16-bit, stereo)
    audio = audio.set_frame_rate(44100)  
    audio = audio.set_sample_width(2)  #16-bit
    audio = audio.set_channels(2)  #stereo

    #save as wav
    audio.export(output_path, format='wav')
    
    return output_path
