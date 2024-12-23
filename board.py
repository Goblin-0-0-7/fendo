import numpy as np

from moves import Move, GameStart, PlaceWall, PlacePawn, MovePawn
from path import Area, findAreas, findOwner

class Board():
    def __init__(self, board_size: int, max_pawns: int):
        # board settings
        self.size = board_size
        self.max_pawns = max_pawns
        # board objects
        self.fields: np.ndarray[Field] = np.empty((board_size, board_size), dtype=Field)
        for i in range(board_size):
            for j in range(board_size):
                self.fields[i, j] = Field(board_size)
                self.fields[i, j].setCoordinates((i, j))
        self.areas: list[Area] = []
        self.pawns1: list[Pawn] = []
        self.pawns2: list[Pawn] = []
        self.moves_list: list[Move]= [GameStart]
        # board states
        self.turn = 1
        self.selection: Pawn = None
        
        self.setStartConfiguration()
                
    def placeWall(self, coordinates: tuple[int, int], direction: str, player: int = 0):
        
        self.fields[coordinates[0], coordinates[1]].placeWall(direction)
        if direction == 'N' and coordinates[1] != 0:
            self.fields[coordinates[0], coordinates[1] - 1].placeWall('S')
        elif direction == 'E' and coordinates[0] != self.size - 1:
            self.fields[coordinates[0] + 1, coordinates[1]].placeWall('W')
        elif direction == 'S' and coordinates[1] != self.size - 1:
            self.fields[coordinates[0], coordinates[1] + 1].placeWall('N')
        elif direction == 'W' and coordinates[0] != 0:
            self.fields[coordinates[0] - 1, coordinates[1]].placeWall('E')
        
        if not player: player = self.turn
        self.moves_list.append(PlaceWall(coordinates, direction, player))
        
    def placePawn(self, coordinates: tuple[int, int], player: int = None):
        if not player: player = self.turn
        
        pawn = Pawn(player, coordinates)
        pawn_list = self.pawns1 if player == 1 else self.pawns2
        
        if len(pawn_list) >= self.max_pawns:
            print('Max number of pawns reached')
            return
        
        if self.fields[coordinates[0], coordinates[1]].addPawn(pawn):
            if player == 1:
                self.pawns1.append(pawn)
            elif player == 2:
                self.pawns2.append(pawn)
        self.moves_list.append(PlacePawn(coordinates, player))
    
    def movePawn(self, start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], player = None, undo = False):
        if not player: player = self.turn
        pawn_list = self.pawns1 if player == 1 else self.pawns2
        for pawn in pawn_list:
            if pawn.coordinates == start_coordinates:
                if self.fields[end_coordinates[0], end_coordinates[1]].addPawn(pawn):
                    pawn.setCoordinates(end_coordinates)
                    self.fields[start_coordinates[0], start_coordinates[1]].removePawn()
                    if not undo:
                        self.moves_list.append(MovePawn(start_coordinates, end_coordinates, player))
    
    def removeWall(self, coordinates: tuple[int, int], direction: str):
        self.fields[coordinates[0], coordinates[1]].removeWall(direction)
        if direction == 'N' and coordinates[1] != 0:
            self.fields[coordinates[0], coordinates[1] - 1].removeWall('S')
        elif direction == 'E' and coordinates[0] != self.size - 1:
            self.fields[coordinates[0] + 1, coordinates[1]].removeWall('W')
        elif direction == 'S' and coordinates[1] != self.size - 1:
            self.fields[coordinates[0], coordinates[1] + 1].removeWall('N')
        elif direction == 'W' and coordinates[0] != 0:
            self.fields[coordinates[0] - 1, coordinates[1]].removeWall('E')
        
    def removePawn(self, coordinates: tuple[int, int]):
        for pawn in self.pawns1:
            if pawn.coordinates == coordinates:
                self.pawns1.remove(pawn)
        for pawn in self.pawns2:
            if pawn.coordinates == coordinates:
                self.pawns2.remove(pawn)
        self.fields[coordinates[0], coordinates[1]].removePawn()
    
    
    def selectPawn(self, coordinates: tuple[int, int], player = None):
        ''' Works like toggle selection '''
        if not player: player = self.turn
        pawn_list = self.pawns1 if player == 1 else self.pawns2
        for pawn in pawn_list:
            if pawn.coordinates == coordinates:
                if self.selection:
                    if self.selection == pawn:
                        self.clearSelection()
                    else:
                        self.clearSelection()
                        self.selection = pawn
                        pawn.selected = True
                else:
                    self.selection = pawn
                    pawn.selected = True                

    
    def getSelection(self):
        return self.selection
    
    def clearSelection(self):
        if self.selection:
            self.selection.selected = False
        self.selection = None
    
    def isOccupied(self, coordinates: tuple[int, int]):
        if self.fields[coordinates[0], coordinates[1]].pawn:
            return True
        else:
            return False
    
    def getPawns(self, player: int):
        if player == 1:
            return self.pawns1
        elif player == 2:
            return self.pawns2
        else:
            raise ValueError('Invalid player number')
    
    def undoMove(self):
        if len(self.moves_list) > 0:
            move = self.moves_list.pop()
            if isinstance(move, PlaceWall):
                self.removeWall(move.coordinates, move.direction)
                self.turn = 2 if self.turn == 1 else 1
            elif isinstance(move, PlacePawn):
                self.removePawn(move.coordinates)
                self.turn = 2 if self.turn == 1 else 1
            elif isinstance(move, MovePawn):
                self.movePawn(move.end_coordinates, move.start_coordinates, move.player, undo = True)
            elif isinstance(move, GameStart):
                self.moves_list = [GameStart()]

    
    def evaluateFields(self):
        ''' Updates the Areas, Fields and their corresponding owners '''
        self.areas = findAreas(list(self.fields.flatten()), self.fields)
        for area in self.areas:
            owner = findOwner(area)
            area.setOwner(owner)
            for field in area.getFields():
                field.setOwner(owner)
    
    def getState(self):
        state = {
            'size': self.size,
            'turn': self.turn,
            'pawns1': self.pawns1,
            'pawns2': self.pawns2,
            'fields': self.fields,
            'moves_list': self.moves_list
        }
        return state
    
    def getTurn(self):
        return self.turn
    
    def endTurn(self):
        self.turn = 2 if self.turn == 1 else 1
        self.clearSelection()
    
    def setStartConfiguration(self):
        self.placePawn((0, self.size // 2), 1)
        self.placePawn((self.size - 1, self.size // 2), 2)
        self.turn = 1
    
    def cleanBoard(self):
        self.pawns1 = []
        self.pawns2 = []
        self.clearSelection()
        for i in range(self.size):
            for j in range(self.size):
                self.fields[i, j].cleanField()
        self.moves_list = [GameStart()]
        self.setStartConfiguration()


class Field():  
    def __init__(self, size: int):
        self.board_size = size
        self.coordinates = (-1, -1)
        self.wallN = False
        self.wallE = False
        self.wallS = False
        self.wallW = False
        self.pawn: Pawn = None
        self.owner = 0

    
    def setCoordinates(self, coordinates: tuple[int, int]):
        if coordinates[0] < self.board_size and coordinates[1] < self.board_size:
            self.coordinates = coordinates
        else:
            raise ValueError('Coordinates out of bounds')

    def getCoordinates(self):
        return self.coordinates

    def placeWall(self, direction):
        if direction == 'N' and self.coordinates[1] != 0:
            self.wallN = True
        elif direction == 'E' and self.coordinates[0] != self.board_size - 1:
            self.wallE = True
        elif direction == 'S' and self.coordinates[1] != self.board_size - 1:
            self.wallS = True
        elif direction == 'W' and self.coordinates[0] != 0:
            self.wallW = True
        elif direction == 'N' or direction == 'E' or direction == 'S' or direction == 'W':
            print('Wall out of bounds')
        else:
            raise ValueError('Invalid direction')

    
    def addPawn(self, pawn: int):
        if self.pawn is None:
            self.pawn = pawn
            return True
        else:
            print('Field already has a pawn')
            return False
        
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
        
    def removePawn(self):
        self.pawn = None
    
    def getWall(self, direction):
        match direction:
            case 'N':
                return self.wallN
            case 'E':
                return self.wallE
            case 'S':
                return self.wallS
            case 'W':
                return self.wallW
            case _:
                raise ValueError('Invalid direction')
    
    def getPawn(self):
        return self.pawn
    
    def setOwner(self, owner: int):
        if owner != 0 and owner != 1 and owner != 2:
            raise ValueError('Invalid player number')
        self.owner = owner
    
    def getOwner(self):
        return self.owner
    
    def getNorth(self) -> 'Field':
        if self.coordinates[1] != 0:
            return self.coordinates[0], self.coordinates[1] - 1
        else:
            return None
    
    def getEast(self) -> 'Field':
        if self.coordinates[0] != self.board_size - 1:
            return self.coordinates[0] + 1, self.coordinates[1]
        else:
            return None
    
    def getSouth(self) -> 'Field':
        if self.coordinates[1] != self.board_size - 1:
            return self.coordinates[0], self.coordinates[1] + 1
        else:
            return None

    def getWest(self) -> 'Field':
        if self.coordinates[0] != 0:
            return self.coordinates[0] - 1, self.coordinates[1]
        else:
            return None
    
    def getNeighbour(self, direction: str) -> 'Field':
        match direction:
            case 'N':
                return self.getNorth()
            case 'E':
                return self.getEast()
            case 'S':
                return self.getSouth()
            case 'W':
                return self.getWest()
            case _:
                raise ValueError('Invalid direction')
    
    def cleanField(self):
        self.removeWall('N')
        self.removeWall('E')
        self.removeWall('S')
        self.removeWall('W')
        self.removePawn()
        
class Pawn():
    def __init__(self, player: int, coordinates: tuple[int, int]):
        if player != 1 and player != 2:
            raise ValueError('Invalid player number')
        self.player = player
        self.coordinates = coordinates
        self.selected = False
    
    def getPlayer(self):
        return self.player
    
    def setCoordinates(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates
        
    def getPosition(self):
        return self.coordinates