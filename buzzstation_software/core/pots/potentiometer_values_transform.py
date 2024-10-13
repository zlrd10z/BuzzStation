x_min = -0.070
x_max = 4.096

def scale_transform(y_min, y_max, x):
	y = ((x - x_min) * (y_max - y_min)) / (x_max - x_min)
	y += y_min
	return y

bpm_from_potentiometer2 = lambda pot_value: scale_transform(y_min = 30, y_max = 260, x = pot_value)
swing_from_potentiometer1 = lambda pot_value: scale_transform(y_min = -1, y_max = 100, x = pot_value)
volume_from_potentiometer0 = lambda pot_value: scale_transform(y_min = -1, y_max = 100, x = pot_value)
count_time_per_quarter = lambda bpm_value: 60 / bpm_value	
