from collections import namedtuple
from .pots import potentiometers
from .pots import potentiometer_values_transform
from .song_data import SongData


def pots_operations(song_data):
	while True:
		pots_values = potentiometers.return_potentiometers_values()

		bpm_old_value = song_data.get_data("bpm")
		bpm_new_value = int(potentiometer_values_transform.bpm_from_potentiometer2(pots_values[2]))
		if bpm_new_value - bpm_old_value > 1 or bpm_old_value - bpm_new_value > 1:
			bpm = bpm_new_value
			timeBetweenQuarterNotes = potentiometer_values_transform.count_time_per_quarter(bpm)
			song_data.put_data("bpm", bpm)
			song_data.put_data("timeBetweenQuarterNotes", timeBetweenQuarterNotes)

		swing_old_value = song_data.get_data("swing")
		swing_new_value = int(potentiometer_values_transform.swing_from_potentiometer1(pots_values[1]))
		if swing_new_value - swing_old_value > 1 or swing_old_value - swing_new_value > 1:
			swing = swing_new_value
			song_data.put_data("swing", swing)

		bvol_old_value = song_data.get_data("bvol")
		bvol_new_value = int(potentiometer_values_transform.volume_from_potentiometer0(pots_values[0]))
		if bvol_new_value - bvol_old_value > 1 or bvol_old_value - bvol_new_value > 1:
			bvol = bvol_new_value
			song_data.put_data("bvol", bvol)
