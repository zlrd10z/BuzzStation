import RPi.GPIO as GPIO
import time
import pickle
from pathlib import Path
import os
from datetime import datetime
from datetime import timedelta
import threading


class Keypad:
    queue = None
    GPIO.setmode(GPIO.BCM)
    # Default settings:
    cols = (26, 5, 13)
    rows = (19, 11, 0, 6)
    path_stored_config = os.path.dirname(__file__) + '/sorted_pins'
    lock = threading.Lock()

    # If file with non-default setting exits, load this settings:
    if os.path.exists(path_stored_config):
        with open(path_stored_config, 'rb') as config_to_load:
            sorted_pins = pickle.load(config_to_load)
            cols = sorted_pins[0]
            rows = sorted_pins[1]

    keys = (
    ('1', '2', '3'),
    ('4', '5', '6'),
    ('7', '8', '9'),
    ('*', '0', '#')
    )

    def __init__(self):
        self.pins_setup()

    def pins_setup(self):
        for i in range(len(self.cols)):
            GPIO.setup(self.cols[i], GPIO.OUT)
        for i in range(len(self.rows)):
            GPIO.setup(self.rows[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def check_keys(self):
        try:
            key = '' # if no key pressed, return empty string
            for i in range(len(self.cols)):
                GPIO.output(self.cols[i], GPIO.LOW)
                time.sleep(0.01)
                for j in range(len(self.rows)):
                    if not GPIO.input(self.rows[j]):
                        time.sleep(0.01)
                        if not GPIO.input(self.rows[j]):
                            key = self.keys[j][i]
                        while not GPIO.input(self.rows[j]):
                            pass
                GPIO.output(self.cols[i], GPIO.HIGH)
                time.sleep(0.01)
            return key
        except Exception as e:
            print(e)
            GPIO.cleanup()

    # Detects row pin and col pin for selected pressed key
    def detect_rol_col(self, key, suspected_cols, suspected_rows):
        if not isinstance(suspected_cols, list):
            suspected_cols = [suspected_cols]
        if not isinstance(suspected_rows, list):
            suspected_rows = [suspected_rows]

        print('='*60)
        input(f'Press [{key}] on keypad, then press [enter] key on keyboard to continue.')
        for c in range(len(suspected_cols)):
            GPIO.setup(suspected_cols[c], GPIO.OUT)
            GPIO.output(suspected_cols[c], GPIO.LOW)
            for r in range(len(suspected_rows)):
                if suspected_rows[r] == suspected_cols[c]:
                    continue #same pin
                GPIO.setup(suspected_rows[r], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                time.sleep(0.1)
                if not GPIO.input(suspected_rows[r]):
                    pins = [suspected_cols[c], suspected_rows[r]]
                    print(pins)
                    return pins
            GPIO.output(suspected_cols[c], GPIO.HIGH)
            time.sleep(0.1)

    '''
    This method, if the keyboard has been connected to a good range of pins,
    but the connections in this range to the keypad may be mixed,
    detects (user interaction needed) which pins should be assigned as rows, which as columns,
    and sorts them accordingly, so that when the key [1] is pressed,
    the method reads correctly that the key [1] has just been pressed, and so on.
    '''

    def detect_colls_rows(self):
        unsorted_pins = list(self.cols) + list(self.rows)
        rows = []
        cols = []
        
        # Search for column and row for [1] key, not knowing which one is which:
        temp_pins = self.detect_rol_col(1, unsorted_pins, unsorted_pins)

        # To determine which pin is column pin, detect pin and col for key [4] in the same column:
        temp_pins_2 = self.detect_rol_col(4, temp_pins, unsorted_pins)

        # Search for the column pin:
        for i in range(len(temp_pins)):
            for j in range(len(temp_pins_2)):
                if temp_pins[i] == temp_pins_2[j]:
                    cols.append(temp_pins[i])
                    temp_pins_2.remove(temp_pins[i])
                    unsorted_pins.remove(temp_pins[i])
                    temp_pins.remove(temp_pins[i])
                    break

        # Update rows list with two discovered pins:
        rows += temp_pins + temp_pins_2

        # Update unosrted pins:
        unsorted_pins = list(set(unsorted_pins) - set(rows))

        # Find row 3 and 4 - key [7] and [*]:
        keys = (7, '*')
        for key in keys:
            temp_pins = self.detect_rol_col(key, cols[0], unsorted_pins)
            unsorted_pins.remove(temp_pins[1])
            rows.append(temp_pins[1])

        # Find col 2:
        temp_pins = self.detect_rol_col(0, unsorted_pins, rows[-1])
        cols.append(temp_pins[0])
        unsorted_pins.remove(temp_pins[0])

        # last pin left unsorted is col 3:
        cols = cols + unsorted_pins

        self.rows = rows
        self.cols = cols
        # Save with picle
        with open(self.path_stored_config, 'wb') as config_to_save:
            sorted_pins = (cols, rows)
            pickle.dump(sorted_pins, config_to_save)

    def test_keys(self):
        while True:
            key = keypad.check_keys()
            if key != '':
                    print('Key: ', key)

if __name__ == '__main__':
    keypad = Keypad()
    while True:
        choice = input('1. Detect colls and rows.  \n2. Check if keys working.\nq. Quit\n')
        if choice == '1':
            50*'-'
            try:
                keypad.detect_colls_rows()
                while True:
                    print(50*'-')
                    choice = input('Do you want to test keys?.\ny. \nn. no\n')
                    if choice == 'y':
                        keypad.pins_setup()
                        keypad.test_keys()
                    elif choice == 'n':
                        break
            
            except Exception as e:
                print('Check your connection and please try again.')
                print('Error: ', e)
                GPIO.cleanup()
        
        if choice == '2':
            50*'-'
            keypad.test_keys()
        if choice == 'q':
            break

