# FendoEvents
FIELDHIT = "fieldhit"
WALLHIT = "wallhit"
BUTTONHIT = "buttonhit"

class FendoEvent():
    
    def __init__(self):
        ...
        
class WallEvent(FendoEvent):
    
    def __init__(self, coordinates, direction):
        self.direction = direction