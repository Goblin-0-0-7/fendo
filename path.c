#include "gamerep.h"
#include <stdbool.h> 

//bool checkPathHorizontal(char x, char u, char column, unsigned char horDrc, field_t* boardState){
//    char curX = x;
//    char stepX = horDrc == EAST ? 1 : -1;
//    field_t* curField = boardState + x + 7*column;
//
//    while( curX != u){
//
//        curX += stepX;
//        curField += stepX;
//    }
//    return true;
//}

bool checkPathHorizontal(field_t* startFeld, field_t* endField, unsigned char horDrc){
    char step = horDrc == EAST ? 1 : -1;
    unsigned char wallDrc = (horDrc == EAST) ? WALLWEST : WALLEAST;
    field_t* curField = startFeld + step;

    while ( curField != endField ){
        // Check if wall behind step was blocking path
        if (*curField | wallDrc){
            return false;
        }
        // Check if other pawn is blocking path
        if (*curField | OCCUPIED){
            return false;
        }
        curField += step;
    }
    // Check if wall behind step was blocking path to end field
    if (*curField | wallDrc){
        return false;
    }
    return true;
}

bool checkPathVertical(char y, char v, char row, unsigned char verDrc){
    return true;
}

bool findValidPath(char x, char y, char u, char v, field_t* boardState){
    unsigned char horDrc, verDrc;
    field_t* startField = boardState + x + 7*y;
    field_t* endField = boardState + u + 7*v;

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
    if (checkPathHorizontal(startField, endField, horDrc) && checkPathVertical(y, v, u, verDrc)){
        return true;
    }
    // Check first vertical then horizontal
    if (checkPathVertical(y, v, x, verDrc) && checkPathHorizontal(startField, endField, horDrc)){
        return true;
    }
    return false;
}