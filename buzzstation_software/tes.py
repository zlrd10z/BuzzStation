from libs.keypad import Keypad
from core.midi_params_menu import midi_menu
from core.song_data import SongData

'''
TEMPORARY TEST FUNCTION
'''

keypad = Keypad()
song_data = SongData()

midi_menu.main(keypad, song_data)
