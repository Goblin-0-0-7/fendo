#include "gamerep.h"


/*    def checkLegalMove(self, move: Move, board_state: dict) -> bool:
        if not self.active:
            return True
        match move:
            case PlaceWall():
                return self.checkWallPlace(move.coordinates, move.direction, board_state)
            case PlacePawn():
                return self.checkPawnPlace(move.coordinates, move.player, board_state)
            case MovePawn():
                return self.checkPawnMove(move.start_coordinates, move.end_coordinates, board_state)
            case MovePawnAndWall():
                if self.checkLegalMove(MovePawn(move.start_coordinates, move.end_coordinates, move.player), board_state):
                    # Manipulate board_state to use checkWallPlace
                    board_state['moves_list'].append(MovePawn(move.start_coordinates, move.end_coordinates, move.player))
                    legal = self.checkLegalMove(PlaceWall(move.end_coordinates, move.direction, move.player), board_state)
                    # Undo the manipulation
                    board_state['moves_list'].pop()
                    return legal
                return False
            case _:
                raise ValueError('Invalid move')
 */           

/* Notes: direction is a transferred mask*/
bool checkWallPlace(char x, char y, unsigned char direction, field_t * boardState){
    field_t* field = boardState + x + 7 * y;
    // Check if wall is already placed
    if (*field & direction){
        return false;
    }
    // Check if wall is placed on the edge of the board
    if (y == 0 && direction == NORTH){
        return false;
    }
    if (y == 6 && direction == SOUTH){
        return false;
    }
    if (x == 6 && direction == EAST){
        return false;
    }
    if (x == 0 && direction == WEST) {
        return false;
    }
    // Check if wall placement is next to the previous pawn, moved by the same player
    /* Not needed for AI */
    // Check if field has pawn
    /* Not needed for AI */
    return true;
}


bool checkPawnMove(char x, char y, char u, char v, field_t* boardState){
    field_t* startField = boardState + x + 7*y;
    field_t* endField = boardState + u + 7*v;
    // Check if it is the correct turn
    /* Not needed for AI */
    // Check if the start field has an active pawn (For AI move generation this equals to checking if the start field is already assigned or not)
    if (*startField | ASSIGNED){
        return false;
    }
    // Check if the end field is occupied
    if (*endField | OCCUPIED){
        return false;
    }
    return findValidPath(x, y, u, v, boardState);
}

/*
    def checkPawnMove(self, start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], board_state: dict):
        previous_move = board_state['moves_list'][-1]
        if previous_move.player == board_state['turn']:
            return False
        # Check if the start field has an active pawn
        if not board_state['fields'][start_coordinates[0], start_coordinates[1]].getPawn().isActive():
            return False
        # Check if the end field is occupied
        if board_state['fields'][end_coordinates[0], end_coordinates[1]].getPawn():
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
            if findValidPath(pawn.getCoordinates(), coordinates, board_state['fields']):
                return True
        return False
    */