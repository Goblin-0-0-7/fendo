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