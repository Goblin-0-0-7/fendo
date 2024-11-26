class Move():
    
    def __init__(self):
        ...
        
class PlaceWall(Move):
    
    def __init__(self, coordinates, direction):
        self.coordinates = coordinates
        self.direction = direction
        
class PlacePawn(Move):
    
    def __init__(self, coordinates, pawn):
        self.coordinates = coordinates
        self.pawn = pawn
        
class MovePawn(Move):
    
    def __init__(self, start_coordinates, end_coordinates, pawn):
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.pawn = pawn
    