import pygame

from colors import *

class HUD():
    
    def __init__(self):
        self.buttons: list[Button] = []
        self.texts: list[Text] = []
        self.rects: list[Rectangle] = []
    
    def draw(self, screen: pygame.Surface):
        for item in self.getItems():
            item.draw(screen)
    
    def getItems(self):
        return self.buttons + self.texts + self.rects
    
    def addButton(self, button):
        self.buttons.append(button)
        
    def addText(self, text):
        self.texts.append(text)
        
    def addRect(self, rect):
        self.rects.append(rect)

class Text():
    
    def __init__(self, top: float = None, left: float = None, text: str = None, font_size: float = None,
                 color: tuple[int, int, int] = None, on_update: callable = None):
        self.top = top
        self.left = left
        self.text = text
        self.font_size = font_size
        self.color = color
        self.on_update = on_update
    
    def draw(self, screen: pygame.Surface):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.color)
        screen.blit(text, (self.left, self.top))
    
    def setText(self, text):
        self.text = text
        
    def setColor(self, color):
        self.color = color
        
    def setTop(self, top):
        self.top = top
        
    def setLeft(self, left):
        self.left = left
        
class Rectangle():
    
    def __init__(self, top: float = None, left: float = None, width: float = None, height: float = None,
                 color: tuple[int, int, int] = None):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.height))
        
    def setColor(self, color):
        self.color = color
        
    def setTop(self, top):
        self.top = top
        
    def setLeft(self, left):
        self.left = left
        
    def setWidth(self, width):
        self.width = width
        
    def setHeight(self, height):
        self.height = height

class Button():
    
    def __init__(self, top: float = None, left: float = None, width: float = None, height: float = None,
                 text: str = None, font_size: float = None, color: tuple[int, int, int] = None, action: callable = None):
        # TODO: Button should consist of a rectangle and a text
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.color = color
        self.action = action

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.height))
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.left + self.width/4, self.top + self.height/4))

    def setAction(self, action):
        self.action = action
    
    def setText(self, text):
        self.text = text
        
    def setColor(self, color):
        self.color = color
        
    def setTop(self, top):
        self.top = top
        
    def setLeft(self, left):
        self.left = left
        
    def setWidth(self, width):
        self.width = width
        
    def setHeight(self, height):
        self.height = height