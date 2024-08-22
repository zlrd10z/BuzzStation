from gui import gui_tracker
from libs.keypad import Keypad
from core.data_storage import DataStorage


def main(keys, data_storage):
	tracker_cursor = [0, 0, 0]
	
	while True:
		
		if tracker_cursor[0] == 0 and tracker_cursor[2] != 0: tracker_cursor[2] = 0
		
		key = keys.check_keys()
		if key != '':
			samples = data_storage.get_data("samples")
			
			# [Escape] key - back to playlist:
			if key == '1':
				break
			
			# direction key - down:
			if key == '8':
				if tracker_cursor[1] + 1 < 17:
					tracker_cursor[1] += 1
				else: tracker_cursor[1] == -1
			
			# direction key - up:
			if key == '2':
				if tracker_cursor[1] - 1 > -1:
					tracker_cursor[1] -= 1
					if tracker_cursor == 0:
						tracker_cursor[2] = 0
				else: tracker_cursor[1] == 16
			
			# direction key = right:
			if key == '6':
				# If actual selected sample is not empty, user can move to pick next empty sample:
				if tracker_cursor[1] == 0 and samples[tracker_cursor[0]] != 'Empty':
					tracker_cursor[0] += 1
				
				# If cursor is on playlist and next track from the right is choosen, let user to move cursor to next sample playlist:
				if tracker_cursor[2] == 0:
					tracker_cursor[2] += 1
				elif tracker_cursor[2] == 1:
					if tracker_cursor[1] != 0 and samples[tracker_cursor[0] + 1] != 'Empty':
						tracker_cursor[0] += 1

			if key == '4':
				if tracker_cursor[1] == 0 and tracker_cursor[0] - 1 >= 0:
					tracker_cursor[0] -= 1
					
				elif tracker_cursor[1] != 0:
					if tracker_cursor[2] == 1:
						tracker_cursor[2] -= 1
					elif tracker_cursor[2] == 0:
							tracker_cursor[2] = 1
							tracker_cursor[0] -= 1			
	
if __name__ == "__main__":
	keys = Keypad()
	data_storage = DataStorage()
	main(keys, data_storage)
