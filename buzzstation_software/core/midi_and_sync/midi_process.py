from core.midi_and_sync import midi_output1
from core.midi_and_sync import midi_output2and3

# This function will works as another process
def midi_sender(queue):
    while True:
        data = queue.get()
        option = data[0]
        midi_data = data[1]
        match option:
            ## Send signal all notes off to all channels on all outputs:
            case 0:
                # Output 2 and 3: Arduino revice this byte, and then sendind proper all notes off signals to output 2 and 3
                midi_output2and3.send_data_to_arduino(bytes([247])) 
                # Output 1:
                midi_output1.all_notes_off()
            case 1:
                midi_output1.send_data(midi_data)
            case 2:
                midi_output2and3.send_data_to_arduino(midi_data)

# This function stays in main process and comunicates with function midi_process:
def send_to_midi_proc(queue, option, data=None):
    match option:
        case 'all notes off':
            data = (0, data) #None as tuple padding
        case 'output 1':
            data = (1, data)
        case 'output 2 and 3':
            data = (2, data)
        case _:
            #prevent locking
            return None
    queue.put(data)
