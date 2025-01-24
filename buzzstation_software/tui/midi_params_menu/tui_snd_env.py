from tui import scrmx
from tui import sliders

def main(percentages, slider_selected):
    screen_matrix = scrmx.create_screen_matrix()
    scrmx.fill_matrix(screen_matrix)
    scrmx.bg_color(screen_matrix)
    scrmx.draw_box(screen_matrix)
    scrmx.draw_title(screen_matrix, "Sound Envelopes:")
    scrmx.draw_instr(screen_matrix, 'Press [►⏸] key to play/pause C5 note.')
    sliders.draw_sliders(screen_matrix=screen_matrix,
                         which_slider_selected=0,
                         ["Attack", 30],
                         ["Decay", 53],
                         ["Sustain", 73],
                         ["Release", 37]
                        )
    scrmx.print_screen_matrix(screen_matrix)

if __name__ == "__main__":
    # Test
    main((37, 50, 70, 97), 1)
