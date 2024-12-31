class Move():
    
    def __init__(self):
        ...
        
class GameStart(Move):
    
    def __str__(self):
        return "GameStart"

class PlaceWall(Move):
    
    def __init__(self, coordinates, direction, player):
        self.coordinates = coordinates
        self.direction = direction
        self.player = player
        
    def __str__(self):
        return f"PlaceWall: [{self.coordinates}, {self.direction}, {self.player}]"
        
class PlacePawn(Move):
    
    def __init__(self, coordinates, player):
        self.coordinates = coordinates
        self.player = player
        
    def __str__(self):
        return f"PlacePawn: [{self.coordinates}, {self.player}]"
        
class MovePawn(Move):
    
    def __init__(self, start_coordinates, end_coordinates, player):
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.player = player
        
    def __str__(self):
        return f"MovePawn: [{self.start_coordinates}, {self.end_coordinates}, {self.player}]"
    
class MovePawnAndWall(Move):
    
    def __init__(self, start_coordinates, end_coordinates, direction, player):
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.direction = direction
        self.player = player
        
    def __str__(self):
        return f"MovePawnAndWall: [{self.start_coordinates}, {self.end_coordinates}, {self.direction}, {self.player}]"