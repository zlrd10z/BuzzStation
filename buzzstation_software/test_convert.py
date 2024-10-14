from core import convert_audio_to_temp

input_path = "/home/obojetnie/samples/fh_kick_lowly.wav"
o_path = convert_audio_to_temp.convert_to_pygame_format(input_path)
print(o_path)
