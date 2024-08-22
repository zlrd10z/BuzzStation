class DataStorage:
	def __init__(self):
		#==================================================
		# Potentiometers:
		self.__bpm = 0
		self.__swing = 0
		self.__bvol = 0
		self.__timeBetweenQuarterNotes = 0
		
		#==================================================
		# Curosrs:
		self.__playlist_cursor = [0, 0]
		
		#==================================================
		# Song data:
		self.__song_playlist = []
		self.__playlist_list_of_instruments = ["Drums"]
		self.__last_added_pattern_numer = 1
		
		#==================================================
		# Pattern data:
		self.__patterns = []

		#patterns order in pattern list, so if the pattern_order list would looks like [3,2], 
		#it means that first l is in pattern is pattern 3 and second list is pattern 2
		self.__patterns_order = [] 
		
		self.__samples = ["Empty"]
		self.__last_added_note = ["C5", "F"]
	
		#==================================================
		# Append instrument list and samples list with 7 * string "Empty":
		for i in range(7):
			self.__playlist_list_of_instruments.append("Empty")
			self.__samples.append("Empty")
	
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

	
	def patternOperations(self, operation, pattern_number, new_pattern = None, index = None):
		result = None
		index = __patterns_order.index(pattern_number)
		
		# Delete pattern from pattern list and pattern order list:
		if operation == "delete_pattern":
			__patterns.pop(index)
			__patterns_order.pop(index)
			
		# Get pattern from list of patterns:	
		elif operation == "get pattern":
			result = __patterns[index]
			result = result[:]
		
		# Update patterns list with new pattern
		elif operation == "update pattern":
			__patterns[index] = new_pattern
		
			
		
		return result
			
			
			
