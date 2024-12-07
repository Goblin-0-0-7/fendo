from moves import Move, PlaceWall, PlacePawn, MovePawn

class Referee():
    
    def __init__(self):
        ...
        
    
    def checkLegalMove(self, move: Move, board_state: dict) -> bool:
        match move:
            case PlaceWall():
                return self.checkWallPlace(move.coordinates, move.direction, board_state)
            case PlacePawn():
                return self.checkPawnPlace(move.coordinates, move.player, board_state)
            case MovePawn():
                return self.checkPawnMove(move.start_coordinates, move.end_coordinates, move.player, board_state)
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
        previous_move = board_state['moves_list'][-1]
        if isinstance(previous_move, MovePawn):
            if previous_move.player == board_state['turn']:
                pawn_coordinates = previous_move.end_coordinates
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
        else:
            return False


    def checkPawnMove(self, start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], player: int, board_state: dict):
        # Check path
        return True
    
    def checkPawnPlace(self, coordinates: tuple[int, int], player: int, board_state: dict):
        previous_move = board_state['moves_list'][-1]
        if isinstance(previous_move, PlacePawn):
            if previous_move.player == player:
                return False
        if isinstance(previous_move, MovePawn):
            return False
        # Check path
        return True