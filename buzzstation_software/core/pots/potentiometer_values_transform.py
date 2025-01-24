from decimal import Decimal


X_MIN = -0.070
X_MAX = 4.095875

def scale_transform(y_min, y_max, x):
    y = ((x - X_MIN) * (y_max - y_min)) / (X_MAX - X_MIN)
    y += y_min
    return y

bpm_from_potentiometer2 = lambda pot_value: scale_transform(y_min = 1, y_max = 200, x = pot_value)
swing_from_potentiometer1 = lambda pot_value: scale_transform(y_min = -52, y_max = 50, x = pot_value)
volume_from_potentiometer0 = lambda pot_value: scale_transform(y_min = -1, y_max = 100, x = pot_value)
count_time_per_quarter = lambda bpm_value: float(Decimal(60) / Decimal(bpm_value)/ 4) 
