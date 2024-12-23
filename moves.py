class Move():
    
    def __init__(self):
        ...
        
class GameStart(Move):
    ...

class PlaceWall(Move):
    
    def __init__(self, coordinates, direction, player):
        self.coordinates = coordinates
        self.direction = direction
        self.player = player
        
class PlacePawn(Move):
    
    def __init__(self, coordinates, player):
        self.coordinates = coordinates
        self.player = player
        
class MovePawn(Move):
    
    def __init__(self, start_coordinates, end_coordinates, player):
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.player = player
    