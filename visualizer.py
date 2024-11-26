import pygame

from board import Board
from hud import HUD, Button
from events import *
from colors import *

BACKGROUND_COLOR = BROWN
FIELD_COLOR = LIGHT_BROWN
WALL_COLOR = BLACK
PLAYER1_COLOR = ORANGE
PLAYER2_COLOR = LIGHT_BLUE

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
        for i in range(self.board.size):
            for j in range(self.board.size):
                field = self.board.fields[i, j]
                
                centerX = self.margin + field.coordinates[0] * self.field_width + self.field_width / 2
                centerY = self.margin + field.coordinates[1] * self.field_width + self.field_width / 2
                radius = (self.field_width / 2 - self.wall_width / 2) / 2
                if field.pawn1:
                    pygame.draw.circle(self.screen, PLAYER1_COLOR, (centerX,centerY), radius)
                if field.pawn2:
                    pygame.draw.circle(self.screen, PLAYER2_COLOR, (centerX, centerY), radius)
    
    
    def outOfBounds(self, pos) -> bool:
        if pos[0] < self.margin or pos[0] > self.screen_width - self.margin or pos[1] < self.margin or pos[1] > self.screen_width - self.margin:
            return True
        return False
    
    def getField(self, pos):
        if self.outOfBounds(pos):
            return (None, False, '') # return button object instead of None
            
        boarderHit = False
        boarderDirection = ''
        
        fieldX = (int)(pos[0] - self.margin) // self.field_width
        fieldY = (int)(pos[1] - self.margin) // self.field_width
        
        topDist = (pos[1] - self.margin) - fieldY * self.field_width
        leftDist = (pos[0] - self.margin) - fieldX * self.field_width
        rightDist = self.field_width - leftDist
        bottomDist = self.field_width - topDist
        
        if topDist < self.wall_width and leftDist > self.wall_width and rightDist > self.wall_width:
            return FendoEvent(WALLHIT, {})
            boarderHit = True
            boarderDirection = 'N'
        elif leftDist < self.wall_width and topDist > self.wall_width and bottomDist > self.wall_width:
            boarderHit = True
            boarderDirection = 'W'
        elif rightDist < self.wall_width and topDist > self.wall_width and bottomDist > self.wall_width:
            boarderHit = True
            boarderDirection = 'E'
        elif bottomDist < self.wall_width and leftDist > self.wall_width and rightDist > self.wall_width:
            boarderHit = True
            boarderDirection = 'S'      
        
        return (self.board.fields[fieldX, fieldY], boarderHit, boarderDirection)
    
    def drawButton(self, top, left, width, height, text, color):
        pygame.draw.rect(self.screen, color, (top, left, width, height))
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, WHITE)
        self.screen.blit(text, (top + width/4, left + height/4))
    
    
    def drawHUD(self):
        for item in self.hud.getItems():
            if isinstance(item, Button):
                self.drawButton(item.top, item.left, item.width, item.height, item.text, item.color)
        
    
    def update(self):
        self.drawBoard()
        self.drawHUD()
        pygame.display.flip()