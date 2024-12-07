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
        
    def setFontsize(self, font_size):
        self.font_size = font_size

    def getText(self):
        return self.text
    
    def getColor(self):
        return self.color
    
    def getTop(self):
        return self.top
    
    def getLeft(self):
        return self.left
    
    def getFontsize(self):
        return self.font_size
        
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

    def getColor(self):
        return self.color
    
    def getTop(self):
        return self.top
    
    def getLeft(self):
        return self.left
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

class Button():
    
    def __init__(self, top: float = None, left: float = None, width: float = None, height: float = None,
                 text: str = None, font_size: float = None, button_color: tuple[int, int, int] = BLACK, text_color: tuple[int, int, int] = WHITE, action: callable = None):
        self.Rect: Rectangle = Rectangle(top, left, width, height, button_color)
        self.Text: Text = Text(top + height/4, left + width/4, text, font_size, text_color)
        self.action = action

    def draw(self, screen: pygame.Surface):
        self.Rect.draw(screen)
        self.Text.draw(screen)

    def setAction(self, action):
        self.action = action
    
    def setText(self, text):
        self.Text.setText(text)
        
    def setTextColor(self, color):
        self.Rect.setColor(color)
        
    def setTextColor(self, color):
        self.Text.setColor(color)
        
    def setButtonTop(self, top):
        self.Rect.setTop(top)
        
    def setButtonLeft(self, left):
        self.Rect.setLeft(left)
        
    def setButtonWidth(self, width):
        self.Rect.setWidth(width)
        
    def setButtonHeight(self, height):
        self.Rect.setHeight(height) 
        
    def setTextTop(self, top):
        self.Text.setTop(top)
        
    def setTextLeft(self, left):
        self.Text.setLeft(left)
    
    def setTextFontsize(self, font_size):
        self.Text.setFontsize(font_size)

    def getAction(self):
        return self.action
    
    def getText(self):
        return self.Text.getText()
    
    def getTextColor(self):
        return self.Text.getColor()
    
    def getButtonColor(self):
        return self.Rect.getColor()
    
    def getButtonTop(self):
        return self.Rect.getTop()
    
    def getButtonLeft(self):
        return self.Rect.getLeft()
    
    def getButtonWidth(self):
        return self.Rect.getWidth()
    
    def getButtonHeight(self):
        return self.Rect.getHeight()
    
    def getTextTop(self):
        return self.Text.getTop()
    
    def getTextLeft(self):
        return self.Text.getLeft()
    
    def getTextFontsize(self):
        return self.Text.getFontsize()