import os
import multiprocessing
import pygame

def get_filenames_in_temp():
    cwd = os.getcwd()
    temp_dir = cwd + '/.temp/'
    return os.listdir(temp_dir)

def get_sample_note_as_two_var(sample_name):
    sample_note = sample_name.split('_')[-1]
    sample_name_no_note = list(sample_name)
    for i in range(len(sample_note)+1):
        sample_name_no_note.pop(-1)
    sample_name_no_note = ''.join(sample_name_no_note)
    return sample_name_no_note, sample_note

# This function meant to be run as another process, 
# so more CPU resources will left for sample_filenames processing
def player_audiofiles(queue_player):
    pygame.mixer.pre_init(44100, -16, 2, 16)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(256)

    channel = 0
    sample_filenames = []
    for i in range(16):
        sample_filenames.append(None)
    filenames_in_temp = get_filenames_in_temp()
    samples = {}

    cwd = os.getcwd()
    temp_dir = cwd + '/.temp/'

    for i in range(16):
        sample_filenames.append(None)
    # Process main loop:
    while True:
        data = queue_player.get()
        match data[0]:
            # Stop playing:
            case 1:
                pygame.mixer.stop()
            # Update sample path:
            case 2:
                sample_number = data[1]
                sample_path = data[2]
                if sample_filenames[sample_number] in samples:
                    samples.pop(sample_filenames[sample_number])
                sample_name = get_sample_note_as_two_var(sample_path)[0]
                sample_filenames[sample_number] = sample_name
                if sample_name not in samples:
                    samples[sample_name] = {}
                samples[sample_name]['C5'] = pygame.mixer.Sound(temp_dir + sample_path)
            # Update paths for all of sample_filenames
            case 3:
                sample_paths = data[1]
                samples = {}
                for i in range(len(sample_paths)):
                    if sample_paths[i] == 'Empty':
                        sample_filenames[i] = None
                    else:
                        sample_path = temp_dir + sample_paths[i]
                        sample_name = get_sample_note_as_two_var(sample_paths[i])[0]
                        sample_filenames[i] = sample_name
                        if sample_name not in samples:
                            samples[sample_name] = {}
                        samples[sample_name]['C5'] = pygame.mixer.Sound(sample_path)
            case 4:
                # Play sample
                playing_data = data[1]
                sample_number = playing_data[0]
                note = playing_data[1]
                vol = playing_data[2]
                sample_filename = sample_filenames[sample_number]
                if sample_filename is not None:
                    channel = pygame.mixer.find_channel()
                    channel.set_volume(vol)
                    channel.play(samples[sample_filename][note])
            case 5:
                # Update samples dictionary with actual temp dir content:
                new_filenames_in_temp = get_filenames_in_temp()
                samples_to_remove = list(set(filenames_in_temp) - set(new_filenames_in_temp))
                samples_to_add = list(set(new_filenames_in_temp) - set(filenames_in_temp))
                for sample_name in samples_to_remove:
                    filename, note = get_sample_note_as_two_var(sample_name)
                    samples[filename].pop(note)
                for sample_name in samples_to_add:
                    filename, note = get_sample_note_as_two_var(sample_name)
                    if filename not in samples:
                        samples[filename] = {}
                    samples[filename][note] = pygame.mixer.Sound(temp_dir+sample_name)
                filenames_in_temp = new_filenames_in_temp
            case 6:
                # Create fresh sample dictionary with samples from temp:
                filenames_in_temp = get_filenames_in_temp()
                for sample_name in filenames_in_temp:
                    filename, note = get_sample_note_as_two_var(sample_name)
                    if filename not in samples:
                        samples[filename] = {}
                    else:
                        samples[filename][note] = pygame.mixer.Sound(temp_dir+sample_name)


# function in this class communicates via queue with player_audiofiles() working in another process
class SendToPlayer:
    def __init__(self, queue_player):
        self.__queue_player = queue_player

    def stop_playing(self):
        queue_player = self.__queue_player
        '''
        option 1: Send communicate to player process that it 
        have to stop playing all of audio files
        '''
        option = 1
        data = (option,)
        queue_player.put(data)

    def update_sample(self, sample_number, new_sample_path):
        queue_player = self.__queue_player
        '''
        option 2: Send communicate, that device should update sample path
        sample number - which sample (and which channel) should be updated
        '''
        option = 2
        data = (option, sample_number, new_sample_path)
        queue_player.put(data)

    def update_all_samples(self, sample_paths):
        queue_player = self.__queue_player
        '''
        option 3: Send communicate, that all of the samples should be replaced,
        with paths to new audiofiles provided.
        '''
        option = 3
        data = (option, sample_paths)
        queue_player.put(data)

    def play_note(self, sample_number, note, vol):
        #print(f'play note {note}')
        queue_player = self.__queue_player
        option = 4
        '''
        option 4: Send info that audio file should be played immediately, 
        sample_number point which sample shoud be played, vol is that
        audio sample volume.
        '''
        note_data = (sample_number, note, vol)
        data = (option, note_data)
        queue_player.put(data)

    def update_nondefault(self):
        queue_player = self.__queue_player
        '''
        option 5: send information to player, that it need to refresh list,
        of temp samples.
        '''
        option = 5
        data = (option,)
        queue_player.put(data)

    def create_new_nondefault(self):
        queue_player = self.__queue_player
        '''
        option 5: send information to player, that it need to refresh list,
        of temp samples.
        '''
        option = 6
        data = (option,)
        queue_player.put(data)
