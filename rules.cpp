#include "gamerep.h"
#include "path.cpp"

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
    if (*startField & ASSIGNED){
        return false;
    }
    // Check if the end field is occupied
    if (*endField & OCCUPIED){
        return false;
    }
    return findValidPath(x, y, u, v, boardState);
}


bool checkPawnPlace(char u, char v, char player, field_t* boardState){
    field_t *placedPawns, *iField;
    char playerPawns, x , y;
    // Select correct pawns
    if (player = 1){
        placedPawns = boardState + PAWNS1NUM;
        playerPawns = PLAYER1PAWN;
    }
    else {
        placedPawns = boardState + PAWNS2NUM;
        playerPawns = PLAYER2PAWN;
    }
    // Check if pawns left (hardcoded max pawns)
    if ((7 - (char)*placedPawns) <= 0){
        return false;
    }
    // Check if PlacePawn is done as only move of the correct turns player
    /* Not needed for AI */
    for (int i = 0; i < 49; i++){
        iField = boardState + i;
        if( !(*iField & ASSIGNED) && (*iField & playerPawns) ){
            x = i % 7;
            y = i / 7;
            if (findValidPath(x, y, u, v, boardState)){
                return true;
            }
        }
    }
    return false;
}