from gui import scrmx

def main(percentages, slider_selected):
    screen_matrix = scrmx.create_screen_matrix()
    scrmx.fill_matrix(screen_matrix)
    scrmx.bg_color(screen_matrix)
    scrmx.draw_box(screen_matrix)
    scrmx.draw_title(screen_matrix, "Sound Envelopes:")
    scrmx.draw_instr(screen_matrix, 'Press [►⏸] key to play/pause C5 note.')
    

    # Sliders:
    slider_names = ['Attack', 'Decay', 'Sustain', 'Release']
    for i in range(4):
        if slider_selected == i:
            is_selected = True
        else:
            is_selected = False
        scrmx.draw_slider(screen_matrix, 3 + 3*i,  slider_names[i], percentages[i], is_selected)

    scrmx.print_screen_matrix(screen_matrix)

if __name__ == "__main__":
    # Test
    main((37, 50, 70, 97), 1)
