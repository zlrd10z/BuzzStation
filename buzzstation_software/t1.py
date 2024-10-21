from core.song_data import SongData
import pickle
import time

#goes thorug playlist and check on which level last pattern was added on the longest track:
def find_last_patt_lvl(longest_track):
    last_pattern_index = None
    for i in range(len(longest_track)-1, -1, -1):
        if longest_track[i] != ' ':
            last_pattern_index = i
            return last_pattern_index

def play_song(song_data):
    playlist = song_data.get_data('song_playlist')
    instruments = song_data.get_data('playlist_list_of_instruments')
    even = False
    
    # The length of the playlist for each instrument can vary, then calculate which is the longest:
    longest_list = max(playlist, key=len)
    playlist_singletrack_index = playlist.index(longest_list)
    last_pattern_index = find_last_patt_lvl(playlist[playlist_singletrack_index])

    # If there is no pattern, don't do anything:
    if last_pattern_index == None: 
        return None

    # for each pattern in playlist for lonest track:
    for p in range(last_pattern_index+1):
        # Get drums pattern:
        if p < len(playlist[0]):
            if(playlist[0][p] != ' '):
                drums_pattern_number = int(playlist[0][p])
                drum_pattern = song_data.drums_pattern_operations(operation = 'get pattern', pattern_number = drums_pattern_number)
            else:
                drum_pattern = None
                
        # for each quarter in pattern, 16 quarter notes per pattern:
        for q in range(16):
            # for each instrument (16 slots for instruments):
            print(f'################test quarter:{q}#############')
            for i in range(16):
                # AUDIO FILES:
                # first slot is for audio samples, rest are for midi instruments, so they are diffrently handled:
                if i == 0:
                    # for sample in quarter (16 slots for samples):
                    for s in range(16):
                        if drum_pattern is not None:
                            if len(drum_pattern[s][q]) > 0:
                                note = drum_pattern[s][q]
                                vol = note[1]
                                # Tests!
                                samples = song_data.get_data('samples')
                                print(samples[s].split('/')[-1], drum_pattern[s][q])
                
                else:
                    # MIDI NOTES:
                    if i < len(playlist):
                        if p < len(playlist[i]):
                            notes = song_data.pianoroll_pattern_operations(operation = 'get notes', 
                                                                           track = i - 1, 
                                                                           pattern_number = playlist[i][p], 
                                                                           quarter = q
                                                                           )
                            print(notes)
            time_between_quarters = 1
            #time_between_quarters = song_data.get_data('time_between_quarter_notes')
            if even:
                time_between_quarters - song_data.get_data('swing')
                even = False
            else:
                time_between_quarters + song_data.get_data('swing')
                even = True
            time.sleep(time_between_quarters)
            
            # Turn off MIDI notes:
            for i in range(1, 17):
                if i < len(playlist):
                    if p < len(playlist[i]):
                        notes_to_turn_off = song_data.pianoroll_pattern_operations(operation = 'get notes', 
                                                                                   track = i - 1, 
                                                                                   pattern_number = playlist[i][p], 
                                                                                   quarter = q, 
                                                                                   target_notes_to_turn_off = True
                                                                                  )
            if not song_data.get_data('is_playing') or not song_data.get_data('is_song_playing'):
                break

if __name__ == '__main__':
    with open('test_song.btp', 'rb') as file_btp:
        song_data = pickle.load(file_btp)
    song_data.put_data('is_playing', True)
    song_data.put_data('is_song_playing', True)
    play_song(song_data)
