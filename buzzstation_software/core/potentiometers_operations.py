from collections import namedtuple
from .pots import potentiometers
from .pots import potentiometer_values_transform
from .song_data import SongData
import subprocess

class PotsAverage:
    def __init__(self):
        self.bpm_avr = 0
        self.swing_avr = 0
        self.vol_avr = 0
        self.bpm = []
        self.swing = []
        self.vol = []

    def put_readings(self):
        pots_readings = potentiometers.return_potentiometers_values()
        self.bpm.append(pots_readings[0])
        self.swing.append(pots_readings[1])
        self.vol.append(pots_readings[2])

    def get_values(self):
        self.put_readings()
        self.bpm_avr = sum(self.bpm) / len(self.bpm)
        self.swing_avr = sum(self.swing) / len(self.swing)
        self.vol_avr = sum(self.vol) / len(self.vol)
        if len(self.bpm) > 5:
            self.bpm.pop(0)
            self.swing.pop(0)
            self.vol.pop(0)
        return (self.bpm_avr, self.swing_avr, self.vol_avr)

def pots_operations(data_for_thread):
    song_data = data_for_thread[0]
    pots_avr = PotsAverage()
    while True:
        pots_values = pots_avr.get_values()
        bpm_old_value = song_data.get_data('bpm')
        bpm_new_value = int(potentiometer_values_transform.bpm_from_potentiometer2(pots_values[2]))
        if bpm_new_value - bpm_old_value > 1 or bpm_old_value - bpm_new_value > 1:
            bpm = bpm_new_value
            time_between_quarter_notes = potentiometer_values_transform.count_time_per_quarter(bpm)
            song_data.put_data('bpm', bpm)
            song_data.put_data('time_between_quarter_notes', time_between_quarter_notes)
        swing_old_value = song_data.get_data('swing')
        swing_new_value = int(potentiometer_values_transform.swing_from_potentiometer1(pots_values[0]))
        if swing_new_value - swing_old_value > 1 or swing_old_value - swing_new_value > 1:
            swing = swing_new_value
            song_data.put_data('swing', swing)
        bvol_old_value = song_data.get_data('bvol')
        bvol_new_value = int(potentiometer_values_transform.volume_from_potentiometer0(pots_values[1]))
        if bvol_new_value - bvol_old_value > 1 or bvol_old_value - bvol_new_value > 1:
            if bvol_new_value < 0:
                bvol_new_value = 0
            bvol = bvol_new_value
            song_data.put_data('bvol', bvol)
            vol_command = f"amixer set Speaker Playback Volume {bvol}%"
            subprocess.Popen(vol_command, shell=True, stdout=subprocess.DEVNULL)

        if song_data != data_for_thread[0]:
            song_data = data_for_thread[0]
            

