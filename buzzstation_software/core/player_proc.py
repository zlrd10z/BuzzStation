import os
import multiprocessing
import pygame

# This function meant to be run as another process, 
# so more CPU resources will left for samples processing
def player_audiofiles(queue_player):
    pygame.mixer.pre_init(44100, -16, 2, 16)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
    channels = [pygame.mixer.Channel(i) for i in range(16)]
    channel = 0
    samples = []
    cwd = os.getcwd()
    temp_dir = cwd + '/.temp/' 
    for i in range(16):
        samples.append(None)
    # Process main loop:
    while True:
        data = queue_player.get()
        match data[0]:
            # Stop playing:
            case 1:
                for channel in channels:
                    channel.stop()
            # Update sample path:
            case 2:
                sample_number = data[1]
                sample_path = data[2]
                sample_path = temp_dir + sample_path + '_C5'
                samples[sample_number] = pygame.mixer.Sound(sample_path)
            # Update paths for all of samples
            case 3:
                sample_paths = data[1]
                for i in range(len(sample_paths)):
                    if sample_paths[i] == 'Empty':
                        samples[i] = None
                    else:
                        sample_path = temp_dir + sample_paths[i] + '_C5'
                        samples[i] = pygame.mixer.Sound(sample_path)
            case 4:
                sample_number = data[1]
                vol = data[2]
                if samples[sample_number] is not None:
                    channels[sample_number].set_volume(vol)
                    channels[sample_number].play(samples[sample_number])

# function in this class communicates via queue with player_audiofiles() working in another process
class SendToPlayer:
    def __init__(self, queue_player):
        self.__queue_player

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

    def update_all_samples(self, sample_paths)
        queue_player = self.__queue_player
        '''
        option 3: Send communicate, that all of the samples should be replaced,
        with paths to new audiofiles provided.
        '''
        option = 3
        data = (option, sample_paths)
        queue_player.put(data)

    def play_note(self, sample_number, vol)
        queue_player = self.__queue_player
        option = 4
        '''
        option 4: Send info that audiofile should be played immediately, 
        sample_number point which sample shoud be played, vol is that
        audio sample volume.
        '''
        note_data = (sample_number, vol)
        data = (option, note_data)
        queue_player.put(data)

