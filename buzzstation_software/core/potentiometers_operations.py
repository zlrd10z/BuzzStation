from collections import namedtuple
from .pots import potentiometers
from .pots import potentiometer_values_transform
from .song_data import SongData
import subprocess


def pots_operations(data_for_thread):
    song_data = data_for_thread['song_data']
    while True:
        pots_values = potentiometers.return_potentiometers_values()
        bpm_old_value = song_data.get_data('bpm')
        bpm_new_value = 0
        for i in range(10):
            pot1_val = potentiometers.return_p1_val()
            bpm_new_value += (potentiometer_values_transform.bpm_from_potentiometer2(pot1_val))
        bpm_new_value = int(bpm_new_value / 10)
        if abs(bpm_new_value - bpm_old_value) > 1:
            bpm = bpm_new_value
            time_between_quarter_notes = potentiometer_values_transform.count_time_per_quarter(bpm)
            song_data.put_data('bpm', bpm)
            song_data.put_data('time_between_quarter_notes', time_between_quarter_notes)
        swing_old_value = song_data.get_data('swing')
        swing_new_value = int(potentiometer_values_transform.swing_from_potentiometer1(pots_values[1]))
        if abs(swing_new_value - swing_old_value) > 1:
            swing = swing_new_value
            song_data.put_data('swing', swing)
        bvol_old_value = song_data.get_data('bvol')
        bvol_new_value = int(potentiometer_values_transform.volume_from_potentiometer0(pots_values[2]))
        if abs(bvol_new_value - bvol_old_value) > 1:
            if bvol_new_value < 0:
                bvol_new_value = 0
            bvol = bvol_new_value
            song_data.put_data('bvol', bvol)
            vol_command = f"amixer set Speaker Playback Volume {bvol}%"
            subprocess.Popen(vol_command, shell=True, stdout=subprocess.DEVNULL)

        # if new song loaded in another thread, change reference: 
        if song_data != data_for_thread['song_data']:
            song_data = data_for_thread['song_data']
            
