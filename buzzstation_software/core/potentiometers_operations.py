from collections import namedtuple
from . import potentiometers
from . import potentiometer_values_transform
from .data_storage import DataStorage
import asyncio

async def potentiometersOperations(data_storage):
	while True:
		pots_values = potentiometers.returnPotentiometersValues()

		bpm_old_value = data_storage.get_data("bpm")
		bpm_new_value = int(potentiometer_values_transform.bpmFromPotentiometer0(pots_values[2]))
		if bpm_new_value - bpm_old_value > 1 or bpm_old_value - bpm_new_value > 1:
			bpm = bpm_new_value
			timeBetweenQuarterNotes = potentiometer_values_transform.countTimePerQuarterNote(bpm)
			data_storage.put_data("bpm", bpm)
			data_storage.put_data("timeBetweenQuarterNotes", timeBetweenQuarterNotes)

		swing_old_value = data_storage.get_data("swing")
		swing_new_value = int(potentiometer_values_transform.swingFromPotentiometer1(pots_values[1]))
		if swing_new_value - swing_old_value > 1 or swing_old_value - swing_new_value > 1:
			swing = swing_new_value
			data_storage.put_data("swing", swing)

		bvol_old_value = data_storage.get_data("bvol")
		bvol_new_value = int(potentiometer_values_transform.volumeFromPotentiometer2(pots_values[0]))
		if bvol_new_value - bvol_old_value > 1 or bvol_old_value - bvol_new_value > 1:
			bvol = bvol_new_value
			data_storage.put_data("bvol", bvol)
		await asyncio.sleep(0.1)
