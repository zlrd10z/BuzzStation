import os, sys
import subprocess
from tui.txtcolor import text_font_color, text_bg_color
from .screen_keyboard import user_input_filename
from libs.keypad import Keypad 
from tui.scrmx import clear_screen


key = ''
selected = 0
q = ''
p = ''
screen_changed = True
option = ''


def hide_cursor():
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()
def show_cursor():
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

audio_formats = ['wav', 'mp3', 'ogg']
def check_audio_format_compatibility(filename):
    filename = filename.split('.')
    file_format = filename[-1]
    compatible = True
    if file_format not in audio_formats:
        compatible = False
    return compatible
    
class displayed_filelist:
    l = []
    def __init__(self, file_list):
        self.l = file_list
    def getList(self):
        l = self.l
        return l
    
def get_linux_output(command):
    result = subprocess.run([command], shell=True, stdout=subprocess.PIPE, text=True)
    result = result.stdout.strip()
    return result

def get_filelist(pwd):
    ls = get_linux_output('ls -p ' + pwd)
    ls = ls.split('\n')
    # Segregate ls output for files and directories
    list_dir = []
    list_files = []
    if '/' in pwd: list_dir.append('…/')
    if option == 'save song':
        list_dir.append('[Create dir]')
        list_dir.append('[Save here as new file]')
    for i in range(len(ls)):
        if '/' in ls[i]: list_dir.append(ls[i])
        else: list_files.append(ls[i])
    ls = list_dir + list_files
    return ls

# Display directory as GUI:
def print_filelist():
    # Function to create information to user the top line of the screen:
    def display_instruction_to_user(option):
        if option == 'sample':
            information_displayed = ' Please choose an audio sample[compatible formats: MP3,WAV,OGG]'
        elif option == 'load song':
            information_displayed = '          Please choose .btp project file to load.'
        elif option == 'save song':
            information_displayed = '          Save song project.'
        elif option == 'controls':
            information_displayed = ' Press [Esc] to abort.'
        number_of_fields_to_fill = 64 - len(information_displayed)
        information_displayed += ' ' * number_of_fields_to_fill
        information_displayed = text_bg_color('blue', information_displayed)
        print(information_displayed)
    
    # display in other color directories, and other color for files for better visibility:
    def chg_txt_print_format(text, mode):
        def adjust_txt_length(text):
            if len(text) > 62:
                text = text[61] + '…'
            return text
        text = adjust_txt_length(text)
        text_len = len(text)
        blue_fill = text_bg_color('blue', ' ')
        
        # Change text color
        if mode == 1:
            text = text_bg_color('grey', text)
        elif mode == 2:
            text = text_font_color('blue', text)
        
        text = blue_fill + text + ' ' * (62 - text_len) + blue_fill
        return text
            
    clear_screen()
    display_instruction_to_user(option)
    ls = q.getList()
    how_many_lines_visible = 15        
    
    # when there is less than 15 lines to display:
    if len(ls) < how_many_lines_visible and len(ls) > 0:
        for i in range(len(ls)):
            toprint = str(ls[i])
            if toprint == str(ls[selected]):
                toprint = chg_txt_print_format(toprint, 1)
            elif '/' in toprint:
                toprint = chg_txt_print_format(toprint, 2)
            else: toprint = chg_txt_print_format(toprint, 3)
            print(toprint)
        free_space = how_many_lines_visible - len(ls)
        for i in range(free_space): print(chg_txt_print_format(' ', 3))
    # when there is more than 15 elemntis in the list, but cursor is on first 15 elements:
    elif selected  < how_many_lines_visible:
        for i in range(how_many_lines_visible):
            toprint = str(ls[i])
            if toprint == str(ls[selected]):
                toprint = chg_txt_print_format(toprint, 1)
            elif '/' in toprint:
                toprint = chg_txt_print_format(toprint, 2)
            else: toprint = chg_txt_print_format(toprint, 3)
            print(toprint)
    # when there is more than 15 elemntis in the list, but cursor is on first 15 elements:    
    elif selected == len(ls)-1:
        lastStartingindex = (len(ls)) - how_many_lines_visible
        for i in range(how_many_lines_visible):
            #print(len(ls), lastStartingindex+i)
            toprint = str(ls[lastStartingindex+i])
            if toprint == str(ls[selected]):
                toprint = chg_txt_print_format(toprint, 1)
            elif '/' in toprint:
                toprint = chg_txt_print_format(toprint, 2)
            else: toprint = chg_txt_print_format(toprint, 3)
            print(toprint)
    # when there is more than 15 elemntis in the list, and the cursor is in the middle of the list:
    elif selected >= how_many_lines_visible:
        temp_l = []
        for i in range(how_many_lines_visible):
            toprint = str(ls[selected-i])
            if toprint == str(ls[selected]):
                toprint = chg_txt_print_format(toprint, 1)
            elif '/' in toprint:
                toprint = chg_txt_print_format(toprint, 2)
            else: toprint = chg_txt_print_format(toprint, 3)
            temp_l.append(toprint)
        templ_l = temp_l.reverse()
        for i in range(len(temp_l)):
            print(temp_l[i])
    display_instruction_to_user('controls')

class PWD:
    pwd = get_linux_output('pwd')
    def update_pwd(self, pwd):
        self.pwd = pwd

def load_directory(start_dir=''):
    pwd = p.pwd + start_dir
    ls = get_filelist(pwd)
    global q
    q = displayed_filelist(ls)

# main function:
def get_filename(selected_option, keypad):    
    global p
    global screen_changed
    global option
    global selected
    selected = 0
    option = selected_option
    p = PWD()
    if option == 'sample':
        start_dir = '/samples'
    else:
        start_dir = '/saved_songs'
    p.update_pwd(p.pwd + start_dir)
    load_directory()
    k = keypad
    print_filelist()
    
    global key
    path_to_selected_file = None
    while True:
        pressed_key =  k.check_keys()
        if pressed_key != '':
            # Navigation with keypad:
            if pressed_key == '8':
                if selected == len(q.l)-1:
                    selected = 0
                else:
                    selected += 1
            if pressed_key == '2':
                if selected == 0:
                    selected = len(q.l)-1
                else:
                    selected -=1
            if pressed_key == '5':
                # if …/ was selected by user and accepted with [insert] key - linux 'cd ..' command equivalent:
                if q.l[selected] == '…/':
                    pwd = p.pwd
                    pwd = pwd.split('/')
                    new_pwd = ''
                    for i in range(len(pwd)-1):
                        new_pwd += pwd[i] + '/'
                    new_pwd = new_pwd[:len(new_pwd) - 1]
                    p.update_pwd(new_pwd)
                    load_directory()
                elif q.l[selected] == '[Create dir]':
                    pwd = p.pwd
                    dir_name = user_input_filename(True, k)
                    dir_path = pwd + '/' + dir_name
                    os.mkdir(dir_path)
                    load_directory()
                    clear_screen()
                elif q.l[selected] == '[Save here as new file]':
                    pwd = p.pwd
                    created_filename = user_input_filename(False, k)
                    path_to_selected_file = pwd + '/' + created_filename
                    clear_screen()
                    break
                # change directory:
                elif '/' in q.l[selected]:
                    dir = q.l[selected]
                    pwd = p.pwd + '/' + dir[:len(dir)-1]
                    p.update_pwd(pwd)
                    load_directory()
                    selected = 0
                else:
                    filename = q.l[selected]
                    if option == 'sample':
                        if check_audio_format_compatibility(filename) == True:
                            path_to_selected_file = p.pwd +'/'+ filename
                            clear_screen()
                            break
                    # to avoid overwriting important file to user, only .btp extensions are accepted: 
                    if option == 'load song' or option == 'save song':
                        file_extension = filename.split('.')
                        file_extension = file_extension[-1]
                        print(file_extension)
                        if file_extension == 'btp':
                            path_to_selected_file = p.pwd +'/'+ filename
                            clear_screen()
                            screen_changed = False
                            break
            # [Esc] key - abort:
            if pressed_key == '1':
                clear_screen()
                break
            # display on GUI:
            print_filelist()
            
    return path_to_selected_file
