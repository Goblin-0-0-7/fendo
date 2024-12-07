import pygame

from board import Board
from hud import HUD, Button, Text, Rectangle, Axis
from visualizer import Visualizer
from events import FendoEvent, WallEvent, FieldEvent, ButtonEvent, OutOfBoundsEvent
from colors import *

# Settings
pawns = 8
board_size = 7
board_width =  700
screen_width = 900
wall_width = 5
margin = (screen_width - board_width) / 2
global turn
turn = 1


# Usefull parameters
field_width = board_width / board_size - wall_width
axis_vertical_labels = [str(i) for i in range(1, board_size + 1)]
axis_horizontal_labels = [chr(i) for i in range(65, 65 + board_size)]
axis_label_size = int(field_width / 4)

# Initializing
board = Board(board_size, pawns)

# Set up game
board.placePawn((0, 3), 1)
board.placePawn((6, 3), 2)

hud = HUD()
btn_undo = Button(margin/4, margin/4, 0.8*field_width, field_width/3, "Undo", 20, GRAY, WHITE, board.undoMove)
btn_clear = Button(margin/4, margin/4 + field_width/3 + 40, 0.8*field_width, field_width/3, "Clear", 20, BLACK, WHITE, board.cleanBoard)
axis_x_top = Axis(margin - field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_x_bottom = Axis(margin + board_width + field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_y_left = Axis(margin + field_width/2, margin - field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")
axis_y_right = Axis(margin + field_width/2, margin + board_width + field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")

txt_player1pawn_counter = Text(margin/3, margin + board_width/3, f"Player 1 pawns left: {pawns - len(board.getPawns(1))}", 22, ORANGE)
txt_player2pawn_counter = Text(margin/3, margin + 2*board_width/3, f"Player 2 pawns left: {pawns - len(board.getPawns(2))}", 22, LIGHT_BLUE)
rect_turn_indentifier = Rectangle(margin/3, margin + 1.8*board_width/3, field_width/5, field_width/5, ORANGE)

hud.addItem(btn_undo)
hud.addItem(btn_clear)
hud.addItem(axis_x_top)
hud.addItem(axis_x_bottom)
hud.addItem(axis_y_left)
hud.addItem(axis_y_right)
hud.addItem(txt_player1pawn_counter)
hud.addItem(txt_player2pawn_counter)
hud.addItem(rect_turn_indentifier)


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
                    action = fendo_event.button.getAction()
                    if action is not None:
                        action()
                        update()
                case OutOfBoundsEvent():
                    pass
             
            visi.update()
   