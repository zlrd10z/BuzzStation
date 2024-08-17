import os, sys
import subprocess
import keyboard
from changeTextColor import changeStringFontColor, changeStringBgColor


def getOutputLinux(command):
	result = subprocess.run([command], shell=True, stdout=subprocess.PIPE, text=True)
	result = result.stdout.strip()
	return result

pwd = getOutputLinux("pwd")
libs_path = pwd[:-3] + "libs"


sys.path.insert(0, libs_path)
from keypad import Keypad
from screenkeyboard import userInputFilename


key = ""
selected = 0
q = ""
p = ""
main_thread = True
screen_changed = True
option = ""

clear = lambda: os.system("clear")

def hide_cursor():
	sys.stdout.write('\033[?25l')
	sys.stdout.flush()
def show_cursor():
	sys.stdout.write('\033[?25h')
	sys.stdout.flush()



audio_formats = ["wav", "ogg", "mp3"]
def checkIsAudioFormatIsCompatible(filename):
	filename = filename.split(".")
	file_format = filename[-1]
	compatible = True
	if file_format not in audio_formats:
		compatible = False
	return compatible
	
class DisplayedFilesList:
	l = []
	def __init__(self, file_list):
		self.l = file_list
	def getList(self):
		l = self.l
		return l

def getFileList(pwd):
	ls = getOutputLinux("ls -p " + pwd)
	ls = ls.split("\n")
	# Segregate ls output for files and directories
	list_dir = []
	list_files = []
	if "/" in pwd: list_dir.append("…/")
	if option == "save song":
		list_dir.append("[Create dir]")
		list_dir.append("[Save here as new file]")
	for i in range(len(ls)):
		if "/" in ls[i]: list_dir.append(ls[i])
		else: list_files.append(ls[i])
	ls = list_dir + list_files
	return ls


def printFileList():
	# Function to create information to user the top line of the screen:
	def displayInstructionToUser(option):
		if option == "sample":
			information_displayed = " Please choose an audio sample[compatible formats: MP3,WAV,OGG]"
		elif option == "load song":
			information_displayed = "          Please choose .btp project file to load."
		elif option == "save song":
			information_displayed = "          Save song project."
		elif option == "controls":
			information_displayed = " Press [*] to abort."
		number_of_fields_to_fill = 64 - len(information_displayed)
		information_displayed += " " * number_of_fields_to_fill
		information_displayed = changeStringBgColor("blue", information_displayed)
		print(information_displayed)

		
	def changeTextPrintingFormat(text, mode):
		def adjustTextLength(text):
			if len(text) > 62:
				text = text[61] + "…"
			return text
		text = adjustTextLength(text)
		text_len = len(text)
		blue_fill = changeStringBgColor("blue", " ")
		
		# Change text color
		if mode == 1:
			text = changeStringBgColor("grey", text)
		elif mode == 2:
			text = changeStringFontColor("blue", text)
		
		text = blue_fill + text + " " * (62 - text_len) + blue_fill
		return text
			
	clear()
	displayInstructionToUser(option)
	ls = q.getList()
	how_many_lines_visible = 15		
	
	# when there is less than 15 lines to display:
	if len(ls) < how_many_lines_visible:
		for i in range(len(ls)):
			toprint = str(ls[i])
			if toprint == str(ls[selected]):
				toprint = changeTextPrintingFormat(toprint, 1)
			elif "/" in toprint:
				toprint = changeTextPrintingFormat(toprint, 2)
			else: toprint = changeTextPrintingFormat(toprint, 3)
			print(toprint)
		free_space = how_many_lines_visible - len(ls)
		for i in range(free_space): print(changeTextPrintingFormat(" ", 3))
	# when there is more than 15 elemntis in the list, but cursor is on first 15 elements:
	elif selected  < how_many_lines_visible:
		for i in range(how_many_lines_visible):
			toprint = str(ls[i])
			if toprint == str(ls[selected]):
				toprint = changeTextPrintingFormat(toprint, 1)
			elif "/" in toprint:
				toprint = changeTextPrintingFormat(toprint, 2)
			else: toprint = changeTextPrintingFormat(toprint, 3)
			print(toprint)
	# when there is more than 15 elemntis in the list, but cursor is on first 15 elements:	
	elif selected == len(ls)-1:
		lastStartingindex = (len(ls)) - how_many_lines_visible
		for i in range(how_many_lines_visible):
			#print(len(ls), lastStartingindex+i)
			toprint = str(ls[lastStartingindex+i])
			if toprint == str(ls[selected]):
				toprint = changeTextPrintingFormat(toprint, 1)
			elif "/" in toprint:
				toprint = changeTextPrintingFormat(toprint, 2)
			else: toprint = changeTextPrintingFormat(toprint, 3)
			print(toprint)
	# when there is more than 15 elemntis in the list, and the cursor is in the middle of the list:
	elif selected >= how_many_lines_visible:
		temp_l = []
		for i in range(how_many_lines_visible):
			toprint = str(ls[selected-i])
			if toprint == str(ls[selected]):
				toprint = changeTextPrintingFormat(toprint, 1)
			elif "/" in toprint:
				toprint = changeTextPrintingFormat(toprint, 2)
			else: toprint = changeTextPrintingFormat(toprint, 3)
			temp_l.append(toprint)
		templ_l = temp_l.reverse()
		for i in range(len(temp_l)):
			print(temp_l[i])

	displayInstructionToUser("controls")

class PWD:
	pwd = getOutputLinux("pwd")
	def update_pwd(self, pwd):
		self.pwd = pwd

def loadDirectory():
	pwd = p.pwd
	ls = getFileList(pwd)
	global q
	q = DisplayedFilesList(ls)

def getFilename(o):	
	global p
	global screen_changed
	global option
	option = o
	p = PWD()
	loadDirectory()
	k = Keypad()
	printFileList()
	

	global key
	global selected
	global main_thread
	path_to_selected_file = None
	while True:
		pressed_key =  k.check_keys()
			
		# Navigation with keypad:
		if pressed_key == '8':
			if selected == len(q.l)-1:
				selected = 0
			else:
				selected += 1

		if pressed_key == "2":
			if selected == 0:
				selected = len(q.l)-1
			else:
				selected -=1

		if pressed_key == "5":
			if q.l[selected] == "…/":
				pwd = p.pwd
				pwd = pwd.split("/")
				new_pwd = ""
				for i in range(len(pwd)-1):
					new_pwd += pwd[i] + "/"
				new_pwd = new_pwd[:len(new_pwd) - 1]
				p.update_pwd(new_pwd)
				loadDirectory()
				
			elif q.l[selected] == "[Create dir]":
				pwd = p.pwd
				dir_name = userInputFilename(True)
				dir_path = pwd + "/" + dir_name
				os.mkdir(dir_path)
				loadDirectory()
				clear()
				
			elif q.l[selected] == "[Save here as new file]":
				pwd = p.pwd
				created_filename = userInputFilename(False)
				path_to_selected_file = pwd + "/" + created_filename
				clear()
				break
				
				
			elif "/" in q.l[selected]:
				dir = q.l[selected]
				pwd = p.pwd + "/" + dir[:len(dir)-1]
				p.update_pwd(pwd)
				loadDirectory()
				selected = 0
				
			else:
				filename = q.l[selected]
				if option == "sample":
					if checkIsAudioFormatIsCompatible(filename) == True:
						path_to_selected_file = p.pwd +"/"+ filename
						clear()
						print(path_to_selected_file)
						break

					
				if option == "song file":
					file_extension = filename.split(".")
					file_extension = file_extension[-1]
					if file_extension == "btp":
						path_to_selected_file = p.pwd +"/"+ filename
						main_thread = False
						clear()
						print(path_to_selected_file)
						screen_changed = False
						break
						
		if pressed_key == "*":
			main_thread = False
			clear()
			break
				
		if pressed_key != "":
			printFileList()
			
	return path_to_selected_file

#test = getFilename("save song")
