class DataStorage:
	def __init__(self):
		# Potentiometers:
		self.__bpm = 0
		self.__swing = 0
		self.__bvol = 0
		self.__timeBetweenQuarterNotes = 0
		
		# Curosrs:
		self.__playlist_cursor = [0, 0]
		
		# Song data:
		self.__song_playlist = []
		self.__playlist_list_of_instruments = ["Drums"]
	
		# Append with instrument list with 7 * string "Empty":
		for i in range(7):
			self.__playlist_list_of_instruments.append("Empty")
	
	# Update requested value:
	def put_data(self, var_name, new_value):
		# Check if attribute exsits:
		if hasattr(self, f'_{self.__class__.__name__}__{var_name}'):
			# check if new value is list, if yes, make a list copy:
			if isinstance(new_value, list):
				new_value = new_value[:]
			# set new value to choosen variable:
			setattr(self, f'_{self.__class__.__name__}__{var_name}', new_value)
			
		else:
			raise AttributeError(f"Attribute '{var_name}' does not exist.")
	
	# Get requested value:
	def get_data(self, var_name):
        # Check if attribute exsits:
		if hasattr(self, f'_{self.__class__.__name__}__{var_name}'):
			# Get value from selected variable
			data_to_return = getattr(self, f'_{self.__class__.__name__}__{var_name}')
			# If data is list, return list's copy
			if isinstance(data_to_return, list):
				data_to_return = data_to_return[:]
			return data_to_return
		
		else:
			raise AttributeError(f"Attribute '{var_name}' does not exist.")
