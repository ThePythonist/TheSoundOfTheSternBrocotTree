#!/usr/bin/python3.8

import pygame, sys, time
from pygame.locals import *
from musical import *
from tools import *
pygame.init()        

zero = (0, 1)
infinity = (1, 0)
sbt = stern_brocot_tree(mediant(zero, infinity), zero, infinity)

rplus = sbt.traverse()

def split(sequence):
    a, b = sequence.x
    return (
        List(a, lambda: split(sequence.n())[0]),
        List(b, lambda: split(sequence.n())[1])
    )

nums, dens = split(rplus)

num_state = State(nums.x)
den_state = State(dens.x)

num_stream = Stream(
    "num",
    nums,
    note_duration=0.5,
    note_delay=0.25,
    octave=1,
    volume=0.2,
    state=num_state
)

den_stream = Stream(
    "den",
    dens,
    note_duration=1,
    note_delay=0.25,
    octave=-2,
    volume=0.3,
    state=den_state
)

num_stream.start()
den_stream.start()


width, height = (640, 360)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Sound of the Stern-Brocot Tree")

fonts = {
    "frac": pygame.font.SysFont("Arial", 50),
    "note": pygame.font.SysFont("Arial", 50),
    "dec": pygame.font.SysFont("Arial", 40)
}

colors = {
    "bg": (245, 232, 255),
    "frac": (0, 0, 0),
    "dec": (0, 0, 0),
    "notes": {
        "A": (255, 0, 81),
        "B": (255, 208, 0),
        "C": (0, 211, 71),
        "D": (172, 0, 208),
        "E": (40, 54, 204),
        "F": (15, 109, 235),
        "G": (16, 14, 24),        
    }
}

frac_line_spacing = 10
frac_line_width = 4

notes = []

notes_panel_height = (fonts["frac"].get_height() + frac_line_spacing) * 2
notes_panel_width = width//2
notes_panel_x = width*0.4
notes_panel = pygame.Surface((notes_panel_width, notes_panel_height))
note_scroll_speed = 200
dec_height = int(height*0.1)
dec_places = 10

class Note:
    def __init__(self, symbol, num):
        self.label = fonts["note"].render(symbol, True, colors["notes"][symbol])
        self.x = notes_panel_width + 1
        self.y = 0 if num else notes_panel_height - self.label.get_height()

last_num_note = last_den_note = None

last_time = time.time()
while True:
    dt = time.time()-last_time
    last_time += dt
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            num_stream.stop()
            den_stream.stop()
            sys.exit()
    
    num, num_note = num_state.get()
    den, den_note = den_state.get()

    if num_note != last_num_note:
        notes.append(Note(num_note, True))
        last_num_note = num_note
    
    if den_note != last_den_note:
        notes.append(Note(den_note, False))
        last_den_note = den_note

    num_label = fonts["frac"].render(str(num), True, colors["frac"])
    den_label = fonts["frac"].render(str(den), True, colors["frac"])

    
    screen.fill(colors["bg"])
    
    screen.blit(num_label, (int(width/4 - num_label.get_width()/2), (height-notes_panel_height)//2))
    screen.blit(den_label, (int(width/4 - den_label.get_width()/2), int(height/2+frac_line_spacing)))
    
    frac_line_length = max(num_label.get_width(), den_label.get_width())
    pygame.draw.line(screen, colors["frac"], (int(width/4 - frac_line_length/2), height//2), (int(width/4 + frac_line_length/2), height//2), frac_line_width)

    notes_panel.fill(colors["bg"])

    for note in notes:
        notes_panel.blit(note.label, (note.x, note.y))
        note.x -= note_scroll_speed * dt

    screen.blit(notes_panel, (notes_panel_x, (height-notes_panel_height)//2))

    dec_label = fonts["dec"].render("{:.{}f}".format(num/den, dec_places), True, colors["dec"])
    screen.blit(dec_label, ((width-dec_label.get_width())//2, dec_height))

    pygame.display.update()