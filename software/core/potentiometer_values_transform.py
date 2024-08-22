x_min = -0.070
x_max = 4.096

def scaleTransform(y_min, y_max, x):
	y = ( (x - x_min) * (y_max - y_min) ) / (x_max - x_min)
	y += y_min
	return y

bpmFromPotentiometer0 = lambda pot_value: scaleTransform(y_min = 30, y_max = 260, x = pot_value)
swingFromPotentiometer1 = lambda pot_value: scaleTransform(y_min = -1, y_max = 100, x = pot_value)
volumeFromPotentiometer2 = lambda pot_value: scaleTransform(y_min = -1, y_max = 100, x = pot_value)
countTimePerQuarterNote = lambda bpm_value: 60 / bpm_value	
