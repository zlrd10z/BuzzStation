# Colors:
FONT_PURPLE = "\033[38;5;93m"
BG_BLUE = "\033[48;5;93m"
RESET = "\033[0m"
BG_GREEN = "\033[48;5;10m"
BG_GREY = "\033[47m"
BG_WHITE = "\033[48;5;15m"
BG_BLACK_GREY = "\033[48;5;235m"
BG_DARK_GREY = "\033[48;5;236m"
BG_LIGHT_GREY = "\033[48;5;237m"
FONT_BLACK = "\033[30m"
FONT_BLUE = "\033[38;5;93m"
FONT_YELLOW = "\033[38;5;226m"
FONT_GREEN = "\033[38;5;10m"

# Change char's background color:
def text_bg_color(color, text):
    colored_string = ""
    if color == "green":
        colored_string = (f"{BG_GREEN}{FONT_BLACK}{text}{RESET}")
    elif color == "blue":
        colored_string = (f"{BG_BLUE}{text}{RESET}")
    elif color == "grey":
        colored_string = (f"{BG_GREY}{FONT_BLACK}{text}{RESET}")
    elif color == "white":
        colored_string = (f"{BG_WHITE}{FONT_BLACK}{text}{RESET}")
    elif color == "black grey":
        colored_string = (f"{BG_BLACK_GREY}{text}{RESET}")
    elif color == "dark grey":
        colored_string = (f"{BG_DARK_GREY}{text}{RESET}")
    elif color == "light grey":
        colored_string = (f"{BG_LIGHT_GREY}{text}{RESET}")
    else: pass
    return colored_string

def text_font_color(color, text):
    colored_string = ""
    if color == "blue":
        colored_string = (f"{FONT_BLUE}{text}{RESET}")
    elif color == "purple":
        colored_string = (f"{FONT_PURPLE}{text}{RESET}")
    elif color == "black":
        colored_string = (f"{FONT_BLACK}{text}{RESET}")
    elif color == "yellow":
        colored_string = (f"{FONT_YELLOW}{text}{RESET}")
    elif color == "green":
        colored_string = (f"{FONT_GREEN}{text}{RESET}")
    return colored_string
