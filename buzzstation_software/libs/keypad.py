import RPi.GPIO as GPIO
import time
import pickle
from pathlib import Path
import os


class Keypad:
    GPIO.setmode(GPIO.BCM)
    # Default settings:
    cols = (26, 0, 5)
    rows = (6, 19, 13, 21)
    path_stored_config = os.path.dirname(__file__) + '/sorted_pins'

    # If file with non-default setting exits, load this settings:
    if os.path.exists(path_stored_config):
        with open(path_stored_config, 'rb') as sorted_pins:
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
    def detect_rol_col(self, key, sel_p=None, pins=None):
        if pins is None:
            number_of_pins = len(self.cols + self.rows)
        else:
            number_of_pins = len(pins)
        input(f'Press [{key}] on keypad, then press [enter] key on keyboard to continue...')
        for p in range(number_of_pins):
            if pins is None:
                pins = self.cols + self.rows
                pins = list(pins)
            if sel_p is not None:
                if p > len(pins) -1:
                    return [-1, -2]
                elif sel_p != pins[p]:
                    continue
            if p in pins:
                pins.remove(p)
            for i in range(len(pins)):
                GPIO.setup(pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(pins[p], GPIO.OUT)
            GPIO.output(pins[p], GPIO.LOW)
            time.sleep(0.1)
            for i in range(len(pins)):
                print(pins[i])
                if not GPIO.input(pins[i]) and pins[p] != pins[i]:
                    time.sleep(0.01)
                    print('='*64)
                    GPIO.output(pins[p], GPIO.HIGH)
                    print(pins[i], pins[p])
                    return [pins[i], pins[p]]
            GPIO.output(pins[p], GPIO.HIGH)
            time.sleep(0.01)


    '''
    This method, if the keyboard has been connected to a good range of pins,
    but the connections in this range to the keypad may be mixed,
    detects (user interaction needed) which pins should be assigned as rows, which as columns,
    and sorts them accordingly, so that when the key [1] is pressed,
    the method reads correctly that the key [1] has just been pressed, and so on.
    '''

    def detect_colls_rows(self):
        pins = self.cols + self.rows
        rows = []
        cols = []
        detect_rol_col = self.detect_rol_col
        # Search for column and row for 1 key, not knowing which one is which:
        pins_temp = detect_rol_col(1)

        '''
        Search for col and row for 4 key, col for keys 4 is the same as for key 2,
        row for [1] and [4] is now known.
        '''
        pins_temp_2 = detect_rol_col(4)
        for i in range(2):
            for j in range(2):
                if pins_temp[i] == pins_temp_2[j]:
                    cols.append(pins_temp[i])
                    ind1 = pins_temp.index(pins_temp[i])
                    ind2 = pins_temp_2.index(pins_temp[i])
                    pins_temp_2.pop(ind2)
                    pins_temp.pop(ind1)
                    rows.append(pins_temp[0])
                    rows.append(pins_temp_2[0])
                    break
            if len(pins_temp) < 2 or len(pins_temp_2) < 2:
                break

        '''
        Search for row with key [7] and row with key [*] (first column keys):
        '''
        for i in range(2):
            keys = (7, '*')
            pins_temp = detect_rol_col(keys[i], cols[0])
            print(pins_temp)
            print('row', rows)
            print('cols', cols)
            if pins_temp is not None:
                pins_temp.remove(cols[0])
                rows.append(pins_temp[0])

        # Now pins are segregatet for cols and rows
        cols = cols + list(set(pins) - set(rows))
        # but two column pins may be mixed up:
        if detect_rol_col(key=8, sel_p=None, pins=[rows[2]]) is None:
            temp_col = cols[1]
            cols[1] = cols[2]
            cols[2] = temp_col
        sorted_pins = [cols, rows]

        self.rows = rows
        self.cols = cols
        # Save with picle
        with open(self.path_stored_config, 'wb') as config_to_save:
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
