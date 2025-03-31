#include "gamerep.h"
#include "path.c"


void assignArea(char x, char y, char player, field_t* curField){
    // check if already assined
    if (curField && ASSIGNED){
        return;
    }
    // Assign current field
    *curField = *curField | player;


    for(char i = 0; i < 4; i++){
        if (*curField && DIRECTIONS[i]){ // check for wall in direction
            continue;
        }
        char nextX = x + DIRECTIONXSTEP[i];
        char nextY = y + DIRECTIONYSTEP[i];
        field_t* nextField = curField + DIRECTIONFIELDSTEP[i];
        assignArea(nextX, nextY, player, nextField);
    }
}


char checkAreaOccupied(char x, char y, field_t* board){
    /* returns
    ** -1 if area is empty
    ** 0 if area is owned by one player
    ** 1 if area is occupied/open
    */

    char areaFlag = -1; // area is empty
    for (int i = 0; i < 49; i++){
        field_t* curField = board + i;
        if (*curField & ASSIGNED){
            continue;
        }
        if (*curField & OCCUPIED){
            char curX = i % 7;
            char curY = i / 7;
            if (curX == x && curY == y){
                areaFlag = 0; // area is owned
                continue; // skip own pawn
            }
            if (findPath(x, y, curX, curY, board)) { // search from probably enclosed pawn to other pawn to reduce search time
                return 1; // area is occupied
            }
        }
    }
    return areaFlag; // no pawns found
}


// Searches while hugging the wall to its right until the goal field is reached
// Uses the fact that in the c representation of the board the edges have boarders
bool findOpenPath(char cur_x, char cur_y, char origin_x, char origin_y, char u, char v, char dir, field_t* curField){
    if (cur_x == u && cur_y == v){
        return true;
    }
    if (cur_x == origin_x && cur_y == origin_y){
        return false;
    }
    if (*curField & DIRECTIONS[dir]){
        return findOpenPath(cur_x, cur_x, origin_x, origin_y, u, v, (dir+1)%4, curField);
    }
    else {
        return findOpenPath(cur_x + DIRECTIONXSTEP[dir], cur_y + DIRECTIONYSTEP[dir], origin_x, origin_y, u, v, (dir+3)%4, curField + DIRECTIONFIELDSTEP[dir]); 
    }
}


// changes the board state
bool checkOpenArea(char x, char y, char dir, field_t* boardState){
    char u, v, player;
    bool area, opsArea;
    field_t *field, *opsField;

    switch (DIRECTIONS[dir]){ // Checking for boarders is not necessary as it is already done in checkWallPlace
        case WALLNORTH:
            u = x;
            v = y - 1;
            break;
        case WALLSOUTH:
            u = x;
            v = y + 1;
            break;
        case WALLEAST:
            u = x + 1;
            v = y;
            break;
        case WALLWEST:
            u = x - 1;
            v = y;
            break;
    }

    field = boardState + x + 7*y;

    // Check for open path from origin to opposite field
    if (findOpenPath(x, y, x, y, u, v, dir, field)){
        return true;
    }

    opsField = boardState + u + 7*v;

    // Check for open area on one and the other side of the wall
    area = checkAreaOccupied(x, y, boardState);
    opsArea = checkAreaOccupied(u, v, boardState);

    if ( (area == -1) || (opsArea == -1) || (area == 1 && opsArea == 1)){ // Both areas are open or one is empty
        return false;
    }

    // already assigned fields here as the occupents are kown
    if (area == 0) {
        player = *field & OCCUPIED; // resolves to PLAYER1PAWN or PLAYER2PAWN
        assignArea(x, y, player, field); // 0xff mean no incoming direction
    }
    if (opsArea == 0) {
        player = *opsField & OCCUPIED; // resolves to PLAYER1PAWN or PLAYER2PAWN
        assignArea(u, v, player, opsField);
    }
    return true;
}

/* Notes: direction is a transferred mask*/
bool checkWallPlace(char x, char y, char direction, field_t * boardState){
    field_t* field = boardState + x + 7 * y;
    // Check if wall is already placed
    if (*field & direction){
        return false;
    }
    // Check if wall is placed on the edge of the board
    if (y == 0 && direction == WALLNORTH){
        return false;
    }
    if (y == 6 && direction == WALLSOUTH){
        return false;
    }
    if (x == 6 && direction == WALLEAST){
        return false;
    }
    if (x == 0 && direction == WALLWEST) {
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
    if (player == 1){
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