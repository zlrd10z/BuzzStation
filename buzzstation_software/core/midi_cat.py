import copy

def append_midi_params():
    midi_misc_settings = [None]
    midi_menu_categories = {'Sound Envelopes' : {'Attack' : 0, 
                                                 'Delay' : 0, 
                                                 'Sustain' : 0, 
                                                 'Release' : 0
                                                },
                            'Filter' : {'Attack' : 0, 
                                        'Delay' : 0, 
                                        'Sustain' : 0, 
                                        'Release' : 0,
                                        'Cutoff' : 0,
                                        'Resonance' : 0,
                                        },
                            'Chorus' : {'Level' : 0, 
                                        'Rate' : 0, 
                                        'Depth' : 0, 
                                        'Feedback' : 0
                                        },
                            'Phaser' : {'Depth' : 0, 
                                        'Rate' : 0, 
                                        'Feedback' : 0, 
                                        }, 
                            'Reverb' : {'Level' : 0, 
                                        'Time' : 0, 
                                        'Pre-Delay' : 0, 
                                        }, 
                            'Delay' : {'Level' : 0, 
                                        'Time' : 0, 
                                        'Feedback' : 0,
                                       } 
                        }
    for i in range(15):
        midi_misc_settings.append(copy.deepcopy(midi_menu_categories))
    return midi_misc_settings
