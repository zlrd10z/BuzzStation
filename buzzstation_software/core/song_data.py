from core.midi_cat import append_midi_params


class SongData:
    def __init__(self):
        #==================================================
        # Potentiometers:
        self.__bpm = 0
        self.__swing = 0
        self.__bvol = 0
        self.__time_between_quarter_notes = 0
        
        # Playing:
        self.__is_playing = False #true - playing, false - pause
        self.__is_song_playing = False #true: playing song, false: playing pattern
        self.__instrument_played = None
        self.__playing_track = 0
        self.__playing_pattern = 1
        self.__playing_song_from_lvl = 0

        #==================================================
        # Curosrs:
        self.__playlist_cursor = [0, 0]
        
        #==================================================
        # Song data:
        self.__song_name = 'No songname'
        self.__song_playlist = []
        self.__playlist_list_of_instruments = ['Drums']
        self.__playlist_list_of_midi_assigned = {}
        self.__last_added_pattern_numer = []
        self.__song_loaded = False
        self.__midi_misc_settings = append_midi_params() #envelopes, filters, effects like reverb

        #==================================================
        # Drums and samples pattern data:
        self.__drums_patterns = {}
        self.__samples = ['Empty', 'Empty']
        self.__samples_temp = ['Empty', 'Empty'] 
        self.__last_changed_sample = None
        self.__samples_volume = [10, 10]
        self.__drums_last_added_note = []

        '''
        samples_not_c5 Dictionary contains track number = {} dictionary for each track.
        If new note non-default(C5) note is added on track, 
        then thers added string of note and octave,
        and counter, how many times sample in not != C5 appears in track.
        Each sample in different note is preconverted to .temp dir, 
        so this will be used for tracking, if sample is not used any more, 
        and can be cleared from temp.
        '''
        self.__samples_not_c5 = {} 
 
        #==================================================
        # Pianoroll patterns:
        self.__pianoroll_patterns = {}
        self.__pianoroll_patterns_notes_to_turn_off = {}
        self.__pianoroll_last_added_note = ['C5', 1, 8]
    
        #==================================================
        for i in range(16):
            self.__last_added_pattern_numer.append(1)
            self.__drums_last_added_note.append(['C5', 'F'])
            self.__samples_not_c5[i] = {}
        #==================================================

        # Append instrument list and samples list with 7 * string 'Empty':
        for i in range(7):
            self.__playlist_list_of_instruments.append('Empty')
            self.__samples.append('Empty')
            self.__samples.append('Empty')
            self.__samples_temp.append('Empty')
            self.__samples_temp.append('Empty')
            self.__samples_volume.append(10)
            self.__samples_volume.append(10)

        # Append with default instruments:
        for midi in range(1, 4):
            for channel in range(1, 17):
                output_and_channel = 'M' + str(midi) + 'c' + str(channel)
                self.__playlist_list_of_midi_assigned[output_and_channel] = ('Acoustic Grand Piano', 1)
                    
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
            raise AttributeError(f'Attribute {var_name} does not exist.')
    
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
            raise AttributeError(f'Attribute {var_name} does not exist.')

    def drums_pattern_operations(self, operation, pattern_number, new_pattern=None):
        result = None
        pattern_number = str(pattern_number)
        
        # Delete pattern from pattern list and pattern order list:
        if operation == 'delete_pattern':
            self.__drums_patterns.pop(pattern_number)
        # Get pattern from list of patterns:    
        elif operation == 'get pattern':
            if pattern_number in self.__drums_patterns:
                result = self.__drums_patterns[pattern_number]
                result = result[:]
            else:
                dummy_pattern = []
                for i in range(16):
                    part = []
                    for i in range(16):
                        part.append([])
                    dummy_pattern.append(part)
                result = dummy_pattern
        # Update patterns list with new pattern
        elif operation == 'create or update pattern':
            self.__drums_patterns[pattern_number] = new_pattern
        elif operation == 'exists':
            if pattern_number in self.__drums_patterns:
                result = True
            else:
                result = False
        
        return result
    
    def pianoroll_pattern_operations(self, operation, track=None, pattern_number=None, 
                                     new_pattern=None, quarter=None, target_notes_to_turn_off=False
    ):
        result = None
        pattern = 'pattern' + str(pattern_number)
        
        patterns_collection = self.__pianoroll_patterns
        if target_notes_to_turn_off:
            patterns_collection = self.__pianoroll_patterns_notes_to_turn_off
        
        if operation == 'get pattern for single track':
            result = patterns_collection[track][pattern]
        elif operation == 'get notes':
            if track in patterns_collection:
                if pattern in patterns_collection[track]:
                    result = patterns_collection[track][pattern][quarter]
            else:
                result = None
        elif operation == 'get number of tracks':
            result = len(patterns_collection)
        elif operation == 'create or update pattern':
            if track not in patterns_collection:
                patterns_collection[track] = {}
            patterns_collection[track][pattern] = new_pattern
        elif operation == 'delete pattern':
            patterns_collection[track].pop(pattern)
        elif operation == 'exists':
            if track in patterns_collection:
                if pattern in patterns_collection[track]:
                    result = True
            else:
                result = False
        
        return result

    def midi_misc_settings_operations(self, option, track, new_value=None, target_title=None):
        result = None
        output_and_channel = self.__playlist_list_of_instruments[track]
        match option:
            case "get":
                if target_title is None:
                    result = self.__midi_misc_settings[output_and_channel]
                else:
                    result = self.__midi_misc_settings[output_and_channel][target_title]
            case "update":
                if new_value is not None:
                    if target_title is None:
                        self.__midi_misc_settings[output_and_channel] = new_value
                    else:
                        self.__midi_misc_settings[output_and_channel][target_title] = new_value
        return result

    def last_added(self, target, track, new_value=None):
        result = None
        if new_value is not None:
            if target == 'playlist':
                self.__last_added_pattern_numer[track] = new_value
            elif target == 'tracker':
                self.__drums_last_added_note[track] = new_value
        else:
            if target == 'playlist':
                result = self.__last_added_pattern_numer[track] 
            elif target == 'tracker':
                result = self.__drums_last_added_note[track]
        return result

    def nondefault_note_counter(self, operation, track=None, note=None, pattern=None):
        def increase(self, track, note):
            if note != 'C5':
                if note not in self.__samples_not_c5[track]:
                    self.__samples_not_c5[track][note] = 1
                    result = True
                else:
                    self.__samples_not_c5[track][note] += 1
                    result = False
            else:
                result = False
            return result

        def decrease(self, track, note):
            if note != 'C5':
                if note in self.__samples_not_c5[track]:
                    if self.__samples_not_c5[track][note] == 1:
                        self.__samples_not_c5[track].pop(note)
                        return note
                    else:
                        self.__samples_not_c5[track][note] -= 1

        result = None
        if track is not None and note is not None:
            if operation == 'increase':
                result = increase(self, track, note)
            elif operation == 'decrease':
                result = [(track, decrease(self, track, note))]
        # Cloning / Removing pattern:
        if pattern is not None:
            #for each track:
            for t in range(len(pattern)):
                # for each quarter:
                for q in range(len(pattern[t])):
                    if len(pattern[t][q]) > 0:
                        note = pattern[t][q][0]
                        if note != 'C5':
                            if operation == 'increase':
                                increase(self, t, note)
                            else:
                                note_to_remove = decrease(self, t, note)
                                if note_to_remove not in result and note_to_remove is not None:
                                    if result is None:
                                        result = []
                                    result.append((t, note_to_remove))
        return result

    def new_nondefaults(self):
        self.__samples_not_c5 = {}
        for i in range(16):
            self.__samples_not_c5[i] = {}
