import pygame

from board import Board
from hud import HUD, Button, Text, Rectangle
from events import FendoEvent, WallEvent, FieldEvent, ButtonEvent, OutOfBoundsEvent
from colors import *

BACKGROUND_COLOR = BROWN
FIELD_COLOR = LIGHT_BROWN
WALL_COLOR = BLACK
PLAYER1_COLOR = ORANGE
PLAYER2_COLOR = LIGHT_BLUE
SELECTED_COLOR = WHITE

class Visualizer:
    
    def __init__(self, screen_width, board_with, margin, wall_width, board: Board, hud: HUD):
        self.board = board
        self.hud = hud
        self.screen_width = screen_width
        self.field_width = (int)((board_with) / board.size)
        self.wall_width = wall_width
        self.margin = margin
        self.initializeBoard(screen_width)
        self.update()
    
    def initializeBoard(self, screen_width):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Fendo")
    
    def drawBoard(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.drawFields()
        self.drawWalls()
        self.drawPawns()
    
    def drawFields(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                field = self.board.fields[i, j]
                
                top = self.margin + field.coordinates[1] * self.field_width + self.wall_width
                left = self.margin + field.coordinates[0] * self.field_width + self.wall_width
                width = self.field_width - 2*self.wall_width
                
                pygame.draw.rect(self.screen, FIELD_COLOR, (top, left, width, width))
        

    def drawWalls(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                field = self.board.fields[i, j]
                
                top = self.margin + field.coordinates[1] * self.field_width
                left = self.margin + field.coordinates[0] * self.field_width
                if field.wallN:
                    pygame.draw.rect(self.screen, WALL_COLOR, (left + self.wall_width, top - self.wall_width, self.field_width - 2*self.wall_width, 2*self.wall_width))
                if field.wallW:
                    pygame.draw.rect(self.screen, WALL_COLOR, (left - self.wall_width, top + self.wall_width, 2*self.wall_width, self.field_width - 2*self.wall_width))
                if field.wallE:
                    pygame.draw.rect(self.screen, WALL_COLOR, (left + self.field_width - self.wall_width, top + self.wall_width, 2*self.wall_width, self.field_width - 2*self.wall_width))
                if field.wallS:
                    pygame.draw.rect(self.screen, WALL_COLOR, (left + self.wall_width, top + self.field_width - self.wall_width, self.field_width - 2*self.wall_width, 2*self.wall_width))
    
    def drawPawns(self,):
        for pawn in self.board.pawns1 + self.board.pawns2:
            centerX = self.margin + pawn.coordinates[0] * self.field_width + self.field_width / 2
            centerY = self.margin + pawn.coordinates[1] * self.field_width + self.field_width / 2
            radius = (self.field_width / 2 - self.wall_width / 2) / 2
            color = PLAYER1_COLOR if pawn.player == 1 else PLAYER2_COLOR
            if pawn.selected:
                pygame.draw.circle(self.screen, SELECTED_COLOR, (centerX, centerY), radius + 5)
            pygame.draw.circle(self.screen, color, (centerX, centerY), radius)
    
    
    def outOfBounds(self, pos) -> bool:
        if pos[0] < self.margin or pos[0] > self.screen_width - self.margin or pos[1] < self.margin or pos[1] > self.screen_width - self.margin:
            return True
        return False
    
    def getEvent(self, pos) -> FendoEvent:
        if self.outOfBounds(pos):
            for item in self.hud.getItems():
                if isinstance(item, Button):
                    if pos[0] > item.left and pos[0] < item.left + item.width and pos[1] > item.top and pos[1] < item.top + item.height:
                        return ButtonEvent(item)
            else:
                return OutOfBoundsEvent()
        else:
            fieldX = (int)(pos[0] - self.margin) // self.field_width
            fieldY = (int)(pos[1] - self.margin) // self.field_width
            
            topDist = (pos[1] - self.margin) - fieldY * self.field_width
            leftDist = (pos[0] - self.margin) - fieldX * self.field_width
            rightDist = self.field_width - leftDist
            bottomDist = self.field_width - topDist
            
            if topDist < self.wall_width and leftDist > self.wall_width and rightDist > self.wall_width:
                return WallEvent((fieldX, fieldY), 'N')
            elif leftDist < self.wall_width and topDist > self.wall_width and bottomDist > self.wall_width:
                return WallEvent((fieldX, fieldY), 'W')
            elif rightDist < self.wall_width and topDist > self.wall_width and bottomDist > self.wall_width:
                return WallEvent((fieldX, fieldY), 'E')
            elif bottomDist < self.wall_width and leftDist > self.wall_width and rightDist > self.wall_width:
                return WallEvent((fieldX, fieldY), 'S')
            else:
                return FieldEvent(self.board.fields[fieldX, fieldY]) 

    def drawText(self, top, left, text, font_size, color):
        font = pygame.font.Font(None, font_size)
        text = font.render(text, True, color)
        self.screen.blit(text, (left, top))


    def drawRectangle(self, top, left, width, height, color):
        pygame.draw.rect(self.screen, color, (left, top, width, height))
    
    def drawButton(self, top, left, width, height, text, font_size, color):
        pygame.draw.rect(self.screen, color, (left, top, width, height))
        font = pygame.font.Font(None, font_size)
        text = font.render(text, True, WHITE)
        self.screen.blit(text, (left + width/4, top + height/4))
    
    
    def drawHUD(self):
        for item in self.hud.getItems():
            if isinstance(item, Button):
                self.drawButton(item.top, item.left, item.width, item.height, item.text, item.font_size, item.color)
            if isinstance(item, Text):
                self.drawText(item.top, item.left, item.text, item.font_size, item.color)
            if isinstance(item, Rectangle):
                self.drawRectangle(item.top, item.left, item.width, item.height, item.color)
        
    
    def update(self):
        self.drawBoard()
        self.drawHUD()
        pygame.display.flip()