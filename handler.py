import pygame
import datetime

from board import Board
from hud import HUD, Button, Text, Rectangle, Axis
from visualizer import Visualizer
from rules import Referee
from ai import Fendoter
from moves import Move, PlaceWall, PlacePawn, MovePawn, MovePawnAndWall
from events import FendoEvent, WallEvent, FieldEvent, ButtonEvent, OutOfBoundsEvent
from colors import *

# Settings
ai = True
ai_player = 2
ai_brain = "random"
save_game = False
pawns = 7
board_size = 7
screen_width = 900
margin = (1/9) * screen_width
board_width = screen_width - 2*margin
wall_width = (1/150) * board_width
player_text_size: int = (int) ((1/35) * screen_width)
button_text_size = (int) ((1/40) * screen_width)
winner_text_size = (int) ((1/7) * screen_width)


# Usefull parameters
field_width = board_width / board_size - wall_width
axis_vertical_labels = [str(i) for i in range(1, board_size + 1)]
axis_horizontal_labels = [chr(i) for i in range(65, 65 + board_size)]
axis_label_size = int(field_width / 4)

# Initializing
board = Board(board_size, pawns)
referee = Referee()
if ai:
    fendoter = Fendoter(ai_player, ai_brain)

# HUD
hud = HUD()
btn_undo = Button(margin/4, margin/4, 0.8*field_width, field_width/3, "Undo", button_text_size, GRAY, WHITE, board.undoMove)
btn_clear = Button(margin/4, margin/4 + field_width/3 + 40, 0.8*field_width, field_width/3, "Clear", button_text_size, BLACK, WHITE, board.cleanBoard)
axis_x_top = Axis(margin - field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_x_bottom = Axis(margin + board_width + field_width/6, margin + field_width/2, board_width, margin, axis_horizontal_labels, BLACK, axis_label_size, "horizontal")
axis_y_left = Axis(margin + field_width/2, margin - field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")
axis_y_right = Axis(margin + field_width/2, margin + board_width + field_width/6, margin, board_width, axis_vertical_labels, BLACK, axis_label_size, "vertical")

txt_player1pawn_counter =   Text(top = margin/3,
                                 left = margin + board_width/3,
                                 text = f"Player 1 pawns left: {pawns - len(board.getPawns(1))}",
                                 font_size = player_text_size,
                                 color = ORANGE)
txt_player2pawn_counter =   Text(top = margin/3,
                                 left = margin + 2*board_width/3,
                                 text = f"Player 2 pawns left: {pawns - len(board.getPawns(2))}",
                                 font_size = player_text_size,
                                 color = LIGHT_BLUE)
txt_player1field_counter =  Text(top = (7/5)*margin + board_width,
                                 left = margin + board_width/4,
                                 text = f"Player 1 fields: {board.getPlayerArea(player = 1)}",
                                 font_size = player_text_size,
                                 color = ORANGE)
txt_player2field_counter =  Text(top = (7/5)*margin + board_width,
                                 left = margin + board_width/2,
                                 text = f"Player 2 fields: {board.getPlayerArea(player = 2)}",
                                 font_size = player_text_size,
                                 color = LIGHT_BLUE)
txt_winner =                Text(top = margin + board_width/2,
                                 left = margin + (1/10)*board_width,
                                 font_size = winner_text_size,
                                 active=False,
                                 color = WHITE)
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
hud.addItem(txt_player1field_counter)
hud.addItem(txt_player2field_counter)
hud.addItem(txt_winner)
hud.addItem(rect_turn_indentifier)
hud.addItem(rect_rules_status)


visi = Visualizer(screen_width, board_width, margin, wall_width, board, hud)

def update():
    board.evaluateFields()
    board.setWinner(checkWin())
    updateTexts()
    rect_turn_indentifier.setColor(ORANGE if board.getTurn() == 1 else LIGHT_BLUE)
    visi.update()

def updateTexts():
    txt_player1pawn_counter.setText(f"Player 1 pawns left: {pawns - len(board.getPawns(1))}")
    txt_player2pawn_counter.setText(f"Player 2 pawns left: {pawns - len(board.getPawns(2))}")
    txt_player1field_counter.setText(f"Player 1 fields: {board.getPlayerArea(player = 1)}")
    txt_player2field_counter.setText(f"Player 2 fields: {board.getPlayerArea(player = 2)}")
    if board.getWinner() != 0:
        txt_winner.setText(f"Player {board.getWinner()} wins!")
        txt_winner.setActive(True)
        if save_game:
            saveGame()
    else:
        txt_winner.setActive(False)
        txt_winner.setText("")

def checkWin() -> int:
    winner = 0
    end = True
    for pawn in (board.getPawns(1) or board.getPawns(2)):
        if pawn.isActive():
            end = False
    if end:
        winner = 1 if board.getPlayerArea(1) > board.getPlayerArea(2) else 2
    return winner

def endTurn():
    board.endTurn()
    update()

def saveGame():
    now = datetime.datetime.now()
    filename = now.strftime("record\%Y%m%d_%H%M%S.txt")
    with open(filename, 'w') as file:
        for move in board.getState()['moves_list']:
            print(move, file=file)

def applyMove(move: Move): #TODO: move to board.py? ; use in loop
    if isinstance(move, PlacePawn):
        board.placePawn(move.coordinates)
    elif isinstance(move, PlaceWall):
        board.placeWall(move.coordinates, move.direction)
    elif isinstance(move, MovePawnAndWall):
        board.movePawn(move.start_coordinates, move.end_coordinates)
        board.placeWall(move.end_coordinates, move.direction)

# Main Loop
running = True
while running:
    if ai and board.getTurn() == ai_player:
        fendoter_move = fendoter.makeMove(board)
        applyMove(fendoter_move)
        endTurn()
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
   