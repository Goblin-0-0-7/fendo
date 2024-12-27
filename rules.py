from moves import Move, PlaceWall, PlacePawn, MovePawn
from board import Field, Pawn
from path import findValidPath

class Referee():
    
    def __init__(self):
        self.active = True
        
    def toggleActive(self):
        self.active = not self.active
        
    def isActive(self):
        return self.active
    
    def checkLegalMove(self, move: Move, board_state: dict) -> bool:
        if not self.active:
            return True
        match move:
            case PlaceWall():
                return self.checkWallPlace(move.coordinates, move.direction, board_state)
            case PlacePawn():
                return self.checkPawnPlace(move.coordinates, move.player, board_state)
            case MovePawn():
                return self.checkPawnMove(move.start_coordinates, move.end_coordinates, board_state)
            case _:
                raise ValueError('Invalid move')
            
    def checkWallPlace(self, coordinates: tuple[int, int], direction: str, board_state: dict):
        # Check if wall is already placed
        if board_state['fields'][coordinates[0], coordinates[1]].getWall(direction):
            return False
        # Check if wall is placed on the edge of the board
        if coordinates[0] == 0 and direction == 'W':
            return False
        if coordinates[0] == board_state['size'] - 1 and direction == 'E':
            return False
        if coordinates[1] == 0 and direction == 'N':
            return False
        if coordinates[1] == board_state['size'] - 1 and direction == 'S':
            return False
        # Check if wall placement is next to the previous pawn, moved by the same player
        pawn_positions = []
        previous_move = board_state['moves_list'][-1]
        if isinstance(previous_move, MovePawn):
            if previous_move.player == board_state['turn']:
                pawn_positions.append(previous_move.end_coordinates)
        else: # PlacePawn or PlaceWall
            if previous_move.player == board_state['turn']:
                return False
            else:
                active_pawns = board_state['pawns1'] if board_state['turn'] == 1 else board_state['pawns2']
                for pawn in active_pawns:
                    pawn_positions.append(pawn.getPosition())
        for pawn_coordinates in pawn_positions:
            if pawn_coordinates == coordinates:
                return True
            if pawn_coordinates == (coordinates[0] - 1, coordinates[1]) and direction == 'W':
                return True
            if pawn_coordinates == (coordinates[0] + 1, coordinates[1]) and direction == 'E':
                return True
            if pawn_coordinates == (coordinates[0], coordinates[1] - 1) and direction == 'N':
                return True
            if pawn_coordinates == (coordinates[0], coordinates[1] + 1) and direction == 'S':
                return True
        return False


    def checkPawnMove(self, start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], board_state: dict):
        previous_move = board_state['moves_list'][-1]
        if previous_move.player == board_state['turn']:
            return False
        if not board_state['fields'][start_coordinates[0], start_coordinates[1]].getPawn().isActive():
            return False
        return findValidPath(start_coordinates, end_coordinates, board_state['fields'])
    
    def checkPawnPlace(self, coordinates: tuple[int, int], player: int, board_state: dict):
        player_pawns: list[Pawn] = board_state['pawns1'] if player == 1 else board_state['pawns2']
        active_pawns = [pawn for pawn in player_pawns if pawn.isActive()]
        
        if board_state['max_pawns'] - len(player_pawns) == 0:
            return False
        
        previous_move = board_state['moves_list'][-1]
        if isinstance(previous_move, PlacePawn):
            if previous_move.player == player:
                return False
        if isinstance(previous_move, MovePawn):
            return False
        for pawn in active_pawns:
            if findValidPath(pawn.getPosition(), coordinates, board_state['fields']):
                return True
        return False
    