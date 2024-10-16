GUI_HEIGHT = 17
GUI_WIDTH = 64

# Create matrix 16 x 64 chars
def create_screen_matrix():
    screen_matrix = []
    for i in range(GUI_HEIGHT):
        screen_matrix.append([])
    return screen_matrix

# Append matrix with spaces characters:
def fill_matrix(screen_matrix):
    for i in range(GUI_HEIGHT):
        for j in range(GUI_WIDTH):
            screen_matrix[i].append(' ')    
    return screen_matrix

# create string from chars matrix (screen_matrix) and print it out
def print_screen_matrix(screen_matrix):
    frame = ''
    for i in range(len(screen_matrix)):
        for j in range(len(screen_matrix[0])):
            frame += screen_matrix[i][j]
    print(frame)
