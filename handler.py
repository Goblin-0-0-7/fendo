import pygame

from board import Board
from hud import HUD, Button, Text
from visualizer import Visualizer
from events import FendoEvent, WallEvent, FieldEvent, ButtonEvent, OutOfBoundsEvent
from colors import *

# Settings
pawns = 8
board_size = 7
board_width =  700
screen_width = 800
wall_width = 5
margin = (screen_width - board_width) / 2

# Initializing
hud = HUD()
board = Board(board_size)
btn_undo = Button(margin/4, margin/4, 2*margin, margin/2, 'Undo', 20, GRAY, board.undoMove)
btn_clear = Button(margin/4, (9/4)*margin + 20, 2*margin, margin/2, 'Clear', 20, BLACK, board.cleanBoard)
txt_player1pawn_counter = Text(margin/4, 2*margin, 'Player 1 pawns: ', 20, ORANGE, board.p)
txt_player2pawn_counter = Text(margin/4, 3*margin, 'Player 2 pawns: ', 20, LIGHT_BLUE)

hud.addButton(btn_undo)
hud.addButton(btn_clear)
hud.addText(txt_player1pawn_counter)
hud.addText(txt_player2pawn_counter)


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
            fendo_event = visi.getEvent(pos)
            match fendo_event:
                case FieldEvent():
                    field = fendo_event.field
                    if event.button == 1:  # Left click
                        board.placePawn(field.coordinates, 1)
                    elif event.button == 3:  # Right click
                        board.placePawn(field.coordinates, 2)
                case WallEvent():
                    coords = fendo_event.coordinates
                    direction = fendo_event.direction
                    if event.button == 1:  # Left click
                        board.placeWall(coords, direction)
                case ButtonEvent():
                    action = fendo_event.button.action
                    if action is not None:
                        action()
                case OutOfBoundsEvent():
                    pass
             
            visi.update()
   