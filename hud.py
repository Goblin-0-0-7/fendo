class HUD():
    
    def __init__(self):
        self.buttons: list[Button] = []
        self.texts = []
    
    def getItems(self):
        return self.buttons + self.texts
    
    def addButton(self, button):
        self.buttons.append(button)

class Button():
    
    def __init__(self, top: float = None, left: float = None, width: float = None, height: float = None,
                 text: str = None, color: tuple[int, int, int] = None, action: function = None):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.action = action

    
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