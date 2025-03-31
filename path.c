#include "gamerep.h"
#include <stdbool.h> 

bool checkPathHorizontal(field_t* startField, char x, char u, unsigned char horDrc){
    char step = horDrc == EAST ? 1 : -1; /* positon step and field step are the same */
    unsigned char wallDrc = (horDrc == EAST) ? WALLWEST : WALLEAST;
    field_t* curField = startField + step;

    while ( x != u ){
        // Check if wall behind step was blocking path
        if (*curField & wallDrc){
            return false;
        }
        // Check if other pawn is blocking path
        if (*curField & OCCUPIED){
            return false;
        }
        curField += step;
        x += step;
    }
    // Check if wall behind step was blocking path to end field
    if (*curField & wallDrc){
        return false;
    }
    return true;
}

bool checkPathVertical(field_t* startField, char y, char v, unsigned char verDrc){
    char pos_step = verDrc == SOUTH ? 1 : -1;
    char field_step = verDrc == SOUTH ? 7 : -7;
    unsigned char wallDrc = (verDrc == SOUTH) ? WALLNORTH : WALLSOUTH;
    field_t* curField = startField + field_step;

    while ( y != v ){
        // Check if wall behind step was blocking path
        if (*curField & wallDrc){
            return false;
        }
        // Check if other pawn is blocking path
        if (*curField & OCCUPIED){
            return false;
        }
        curField += field_step;
        y += pos_step;
    }
    // Check if wall behind step was blocking path to end field
    if (*curField & wallDrc){
        return false;
    }
    return true;
}

bool findValidPath(char x, char y, char u, char v, field_t* boardState){
    unsigned char horDrc, verDrc;
    field_t* startField = boardState + x + 7*y;
    field_t* intermediateFieldHor = startField + (u - x);
    field_t* intermediateFieldVer = startField + 7 * (v - y);

    if ( (u - x) > 0 ){
        horDrc = EAST;
    }
    else {
        horDrc = WEST;
    }

    if ( (v - y) > 0 ){
        verDrc = SOUTH;
    }
    else {
        verDrc = NORTH;
    }

    // Check first horizontal then vertical
    if (checkPathHorizontal(startField, x, u, horDrc) && checkPathVertical(intermediateFieldHor, y, v, verDrc)){
        return true;
    }
    // Check first vertical then horizontal
    if (checkPathVertical(startField, y, v, verDrc) && checkPathHorizontal(intermediateFieldVer, x, u, horDrc)){
        return true;
    }
    return false;
}


char* pathHeuristic(char x, char y, char u,  char v, field_t* field){
    char* nextDirection = (char*)malloc(4 * sizeof(char));

    if (x > u){
        nextDirection[0] = WEST;
        nextDirection[3] = EAST;
    }
    else if (x < u){
        nextDirection[0] = EAST;
        nextDirection[3] = WEST;
    }
    else {
        nextDirection[0] = 0xff;
        nextDirection[3] = 0xff;
    }

    if (y > v){
        nextDirection[1] = NORTH;
        nextDirection[2] = SOUTH;
    }
    else if (y < v){
        nextDirection[1] = SOUTH;
        nextDirection[2] = NORTH;
    }
    else {
        nextDirection[1] = 0xff;
        nextDirection[2] = 0xff;
    }

    return nextDirection;
}


// Uses the fact that in the c representation of the board the edges have boarders
bool findPath(char x, char y, char u, char v, field_t* board){
    bool result = false;
    char* nextDirection;
    if (x == u && y == v){
        return true;
    }

    nextDirection = pathHeuristic(x, y, u, v, board);
    
    field_t* curField = board + x + 7*y;
    for (int i = 0; i < 4; i++){
        if ( (curField && DIRECTIONS[i]) || (nextDirection[i] == 0xff) ){ // check for wall in direction or if direction is invalid
            continue;
        }
        char nextX = x + DIRECTIONXSTEP[i];
        char nextY = y + DIRECTIONYSTEP[i];
        result = findPath(nextX, nextY, u, v, board);
    }
    free(nextDirection);
    return result;

}
