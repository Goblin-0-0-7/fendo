class FendoEvent():
    
    def __init__(self):
        ...
        
class WallEvent(FendoEvent):
    
    def __init__(self, coordinates, direction):
        self.coordinates = coordinates
        self.direction = direction

class FieldEvent(FendoEvent):
    
    def __init__(self, field):
        self.field = field
        
class ButtonEvent(FendoEvent):
    
    def __init__(self, button):
        self.button = button
        
class OutOfBoundsEvent(FendoEvent):
    
    def __init__(self):
        ...