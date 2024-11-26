import numpy as np

BOARDSIZE = 7

class Board():
    def __init__(self, size: int):
        self.size = size
        self.fields = np.empty((size, size), dtype=Field)
        for i in range(size):
            for j in range(size):
                self.fields[i, j] = Field()
                self.fields[i, j].setCoordinates((i, j))
                
    def placeWall(self, coordinates: tuple[int, int], direction: str):
        self.fields[coordinates[0], coordinates[1]].placeWall(direction)
        
    def placePawn(self, coordinates: tuple[int, int], pawn: int):
        self.fields[coordinates[0], coordinates[1]].placePawn(pawn)
        
    def removeWall(self, coordinates: tuple[int, int], direction: str):
        self.fields[coordinates[0], coordinates[1]].removeWall(direction)
        
    def removePawn(self, coordinates: tuple[int, int], pawn: int):
        self.fields[coordinates[0], coordinates[1]].removePawn(pawn)
    
    def cleanBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.fields[i, j].cleanField()


class Field():  
    def __init__(self):
        self.coordinates = (-1, -1)
        self.wallN = False
        self.wallE = False
        self.wallS = False
        self.wallW = False
        self.pawn1 = False
        self.pawn2 = False

    
    def setCoordinates(self, coordinates: tuple[int, int]):
        if coordinates[0] < BOARDSIZE and coordinates[1] < BOARDSIZE:
            self.coordinates = coordinates
        else:
            raise ValueError('Coordinates out of bounds')


    def placeWall(self, direction):
        if direction == 'N' and self.coordinates[1] != 0:
            self.wallN = True
        elif direction == 'E' and self.coordinates[0] != BOARDSIZE - 1:
            self.wallE = True
        elif direction == 'S' and self.coordinates[1] != BOARDSIZE - 1:
            self.wallS = True
        elif direction == 'W' and self.coordinates[0] != 0:
            self.wallW = True
        elif direction == 'N' or direction == 'E' or direction == 'S' or direction == 'W':
            print('Wall out of bounds')
        else:
            raise ValueError('Invalid direction')

    
    def placePawn(self, pawn: int):
        if pawn == 1 and self.pawn2 == False:
            self.pawn1 = True
        elif pawn == 2 and self.pawn1 == False:
            self.pawn2 = True
        elif pawn == 1 and self.pawn2 == True:
            print('Player 2 already placed a pawn here')
        elif pawn == 2 and self.pawn1 == True:
            print('Player 1 already placed a pawn here')
        else:
            raise ValueError('Invalid pawn number')
        
    def removeWall(self, direction):
        if direction == 'N':
            self.wallN = False
        elif direction == 'E':
            self.wallE = False
        elif direction == 'S':
            self.wallS = False
        elif direction == 'W':
            self.wallW = False
        else:
            raise ValueError('Invalid direction')
        
    def removePawn(self, pawn: int):
        if pawn == 1:
            self.pawn1 = False
        elif pawn == 2:
            self.pawn2 = False
        else:
            raise ValueError('Invalid pawn number')
        
    def cleanField(self):
        self.removeWall('N')
        self.removeWall('E')
        self.removeWall('S')
        self.removeWall('W')
        self.removePawn(1)
        self.removePawn(2)