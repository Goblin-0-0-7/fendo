import pygame

from board import Board
from hud import HUD, Button, Text, Rectangle
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
global turn
turn = 1




# Initializing
board = Board(board_size, pawns)

# Set up game
board.placePawn((0, 3), 1)
board.placePawn((6, 3), 2)

hud = HUD()
btn_undo = Button(margin/4, margin/4, 2*margin, margin/2, "Undo", 20, GRAY, board.undoMove)
btn_clear = Button(margin/4, (9/4)*margin + 20, 2*margin, margin/2, "Clear", 20, BLACK, board.cleanBoard)
txt_player1pawn_counter = Text(margin/3, 6*margin, f"Player 1 pawns left: {pawns - len(board.getPawns(1))}", 22, ORANGE)
txt_player2pawn_counter = Text(margin/3, 12*margin, f"Player 2 pawns left: {pawns - len(board.getPawns(2))}", 22, LIGHT_BLUE)
rect_turn_indentifier = Rectangle(margin/3, 10.4*margin, margin/2, margin/2, ORANGE)

hud.addButton(btn_undo)
hud.addButton(btn_clear)
hud.addText(txt_player1pawn_counter)
hud.addText(txt_player2pawn_counter)
hud.addRect(rect_turn_indentifier)


visi = Visualizer(screen_width, board_width, margin, wall_width, board, hud)

def update():
    updateTexts()
    visi.update()

def updateTexts():
    txt_player1pawn_counter.setText(f"Player 1 pawns left: {pawns - len(board.getPawns(1))}")
    txt_player2pawn_counter.setText(f"Player 2 pawns left: {pawns - len(board.getPawns(2))}")

def endTurn():
    global turn
    turn = 2 if turn == 1 else 1
    rect_turn_indentifier.setColor(ORANGE if turn == 1 else LIGHT_BLUE)
    visi.update()


# Main Loop
running = True
while running:
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                endTurn()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            fendo_event = visi.getEvent(pos)
            match fendo_event:
                case FieldEvent():
                    field = fendo_event.field
                    if event.button == 1:  # Left click
                        if board.isOccupied(field.coordinates):
                            board.selectPawn(field.coordinates, turn)
                        else:
                            if board.getSelection():
                                board.movePawn(board.getSelection().coordinates, field.coordinates, turn)
                                board.clearSelection()
                            else:                        
                                board.placePawn(field.coordinates, turn)
                                updateTexts()
                    elif event.button == 3: # Right click
                        endTurn()
                case WallEvent():
                    coords = fendo_event.coordinates
                    direction = fendo_event.direction
                    if event.button == 1:  # Left click
                        board.placeWall(coords, direction)
                        endTurn()
                case ButtonEvent():
                    action = fendo_event.button.action
                    if action is not None:
                        action()
                        update()
                case OutOfBoundsEvent():
                    pass
             
            visi.update()
   