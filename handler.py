import pygame

from board import Board
from hud import HUD, Button, Text, Rectangle, Axis
from visualizer import Visualizer
from rules import Referee
from moves import Move, PlaceWall, PlacePawn, MovePawn
from events import FendoEvent, WallEvent, FieldEvent, ButtonEvent, OutOfBoundsEvent
from colors import *

# Settings
pawns = 7
board_size = 7
screen_width = 650
margin = (1/9) * screen_width
board_width = screen_width - 2*margin
wall_width = (1/150) * board_width
player_text_size: int = (int) ((1/35) * screen_width)


# Usefull parameters
field_width = board_width / board_size - wall_width
axis_vertical_labels = [str(i) for i in range(1, board_size + 1)]
axis_horizontal_labels = [chr(i) for i in range(65, 65 + board_size)]
axis_label_size = int(field_width / 4)

# Initializing
board = Board(board_size, pawns)
referee = Referee()

# HUD
hud = HUD()
btn_undo = Button(margin/4, margin/4, 0.8*field_width, field_width/3, "Undo", 20, GRAY, WHITE, board.undoMove)
btn_clear = Button(margin/4, margin/4 + field_width/3 + 40, 0.8*field_width, field_width/3, "Clear", 20, BLACK, WHITE, board.cleanBoard)
axis_x_top = Axis(margin - field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_x_bottom = Axis(margin + board_width + field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_y_left = Axis(margin + field_width/2, margin - field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")
axis_y_right = Axis(margin + field_width/2, margin + board_width + field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")

txt_player1pawn_counter = Text(margin/3, margin + board_width/3, f"Player 1 pawns left: {pawns - len(board.getPawns(1))}", player_text_size, ORANGE)
txt_player2pawn_counter = Text(margin/3, margin + 2*board_width/3, f"Player 2 pawns left: {pawns - len(board.getPawns(2))}", player_text_size, LIGHT_BLUE)
rect_turn_indentifier = Rectangle(margin/3, margin + 1.8*board_width/3, field_width/5, field_width/5, ORANGE)
rect_rules_status = Rectangle(margin/3, (3/2)*margin + board_width, field_width/5, field_width/5, GREEN)
# add items to HUD
hud.addItem(btn_undo)
hud.addItem(btn_clear)
hud.addItem(axis_x_top)
hud.addItem(axis_x_bottom)
hud.addItem(axis_y_left)
hud.addItem(axis_y_right)
hud.addItem(txt_player1pawn_counter)
hud.addItem(txt_player2pawn_counter)
hud.addItem(rect_turn_indentifier)
hud.addItem(rect_rules_status)


visi = Visualizer(screen_width, board_width, margin, wall_width, board, hud)

def update():
    updateTexts()
    rect_turn_indentifier.setColor(ORANGE if board.getTurn() == 1 else LIGHT_BLUE)
    #board.evaluateFields()
    visi.update()

def updateTexts():
    txt_player1pawn_counter.setText(f"Player 1 pawns left: {pawns - len(board.getPawns(1))}")
    txt_player2pawn_counter.setText(f"Player 2 pawns left: {pawns - len(board.getPawns(2))}")

def endTurn():
    board.endTurn()
    update()

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
            if event.key == pygame.K_r:
                referee.toggleActive()
                rect_rules_status.setColor(GREEN if referee.isActive() else RED)
                update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # Right click
                if not referee.isActive():
                    endTurn()
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                fendo_event = visi.getEvent(pos)
                match fendo_event:
                    case FieldEvent():
                        field = fendo_event.field
                        if board.isOccupied(field.coordinates):
                            board.selectPawn(field.coordinates)
                        else:
                            if board.getSelection():
                                if (referee.checkLegalMove(MovePawn(board.getSelection().coordinates, field.coordinates, board.getTurn()), board.getState())):
                                    board.movePawn(board.getSelection().coordinates, field.coordinates)
                                    board.clearSelection()
                            else:
                                if referee.checkLegalMove(PlacePawn(field.coordinates, board.getTurn()), board.getState()):                        
                                    board.placePawn(field.coordinates)
                                    updateTexts()
                                    endTurn()
                    case WallEvent():
                        coords = fendo_event.coordinates
                        direction = fendo_event.direction
                        if referee.checkLegalMove(PlaceWall(coords, direction, board.getTurn()), board.getState()):
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
   