import pygame

from board import Board
from hud import HUD, Button
from visualizer import Visualizer
from colors import *

# Settings
board_size = 7
board_width =  700
screen_width = 800
wall_width = 5
margin = (screen_width - board_width) / 2

# Adding HUD
hud = HUD()
btn_undo = Button(margin/4, margin/4, margin/2, margin/4, 'Undo', BLACK)
btn_clear = Button(margin/2, margin/4, margin/2, margin/4, 'Clear', BLACK)

hud.addButton(btn_undo)
hud.addButton(btn_clear)

# Initializing
board = Board(board_size)
visi = Visualizer(screen_width, board_width, margin, wall_width, board, hud)



# Main Loop
running = True
while running:
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            field, hit, hit_direction = visi.getField(pos)
            if field is None:
                board.cleanBoard()
            else:
                if hit:
                    if event.button == 1:  # Left click
                        board.placeWall(field.coordinates, hit_direction)
                else:
                    if event.button == 1:  # Left click
                        field.placePawn(1)
                    elif event.button == 3:  # Right click
                        field.placePawn(2)
            visi.update()
   