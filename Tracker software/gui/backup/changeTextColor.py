# Colors:
FONT_PURPLE = "\033[38;5;93m"
BG_BLUE = "\033[48;5;93m"
RESET = "\033[0m"
BG_GREEN = "\033[48;5;10m"
BG_GREY = "\033[47m"
FONT_BLACK = "\033[30m"
FONT_BLUE = "\033[38;5;93m"
FONT_YELLOW = "\033[38;5;226m"
FONT_GREEN = "\033[38;5;10m"

# Change char's background color:
def changeStringBgColor(color, text):
	colored_string = ""
	if color == "green":
		colored_string = (f"{BG_GREEN}{FONT_BLACK}{text}{RESET}")
	elif color == "blue":
		colored_string = (f"{BG_BLUE}{text}{RESET}")
	elif color == "grey":
		colored_string = (f"{BG_GREY}{FONT_BLACK}{text}{RESET}")
	else: pass
	return colored_string

def changeStringFontColor(color, text):
	colored_string = ""
	if color == "blue":
		colored_string = (f"{FONT_BLUE}{text}{RESET}")
	if color == "purple":
		colored_string = (f"{FONT_PURPLE}{text}{RESET}")
	if color == "black":
		colored_string = (f"{FONT_BLACK}{text}{RESET}")
	if color == "yellow":
		colored_string = (f"{FONT_YELLOW}{text}{RESET}")
	if color == "green":
		colored_string = (f"{FONT_GREEN}{text}{RESET}")
	return colored_string

