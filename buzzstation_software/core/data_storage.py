class DataStorage:
	def __init__(self):
		#==================================================
		# Potentiometers:
		self.__bpm = 0
		self.__swing = 0
		self.__bvol = 0
		self.__timeBetweenQuarterNotes = 0
		
		# Playing:
		self.__is_playing = False
		self.__patternmode_is_song_playing = False
		
		#==================================================
		# Curosrs:
		self.__playlist_cursor = [0, 0]
		
		#==================================================
		# Song data:
		self.__song_name = "No songname"
		self.__song_playlist = []
		self.__playlist_list_of_instruments = ["Drums"]
		self.__last_added_pattern_numer = 1
		
		#==================================================
		# Drums and samples pattern data:
		self.__drums_patterns = []

		#patterns order in pattern list, so if the pattern_order list would looks like [3,2], 
		#it means that first l is in pattern is pattern 3 and second list is pattern 2
		self.__drums_patterns_order = [] 
		
		self.__samples = ["Empty", "Empty"]
		self.__samples_volume = [10, 10]
		self.__drums_last_added_note = ["C5", "F"]

	
		#==================================================
		# Append instrument list and samples list with 7 * string "Empty":
		for i in range(7):
			self.__playlist_list_of_instruments.append("Empty")
			self.__samples.append("Empty")
			self.__samples.append("Empty")
			self.__samples_volume.append(10)
			self.__samples_volume.append(10)
	
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

	
	def drumsPatternOperations(self, operation, pattern_number, new_pattern = None):
		result = None
		
		index_in_pattern_order = self.__drums_patterns_order.index(pattern_number)

		
		# Delete pattern from pattern list and pattern order list:
		if operation == "delete_pattern":
			self.__drums_patterns.pop(index_in_pattern_order)
			self.__drums_patterns_order.pop(index_in_pattern_order)
			
		# Get pattern from list of patterns:	
		elif operation == "get pattern":
			result = self.__drums_patterns[index_in_pattern_order]
			result = result[:]
		
		# Update patterns list with new pattern
		elif operation == "update pattern":
			self.__drums_patterns[index_in_pattern_order] = new_pattern
		
		return result
