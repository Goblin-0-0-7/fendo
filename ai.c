#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "dynamicarray.c"
#include "gamerep.h"
#include "rules.c"

size_t depthNodes[4] = {0, 0, 0, 0};
size_t totalNodes = 0;

typedef struct fendoterSettings{
    unsigned int searchDepth;
    int playingMethod;
}fendoterSettings;

void evaluateMoves(move_t* bestMove, field_t* boardState, fendoterSettings* settings);
void playRandom(field_t* board, move_t* bestMove);
int minimax(move_t* bestMove);
int negamax(field_t* board, int depth, int p, move_t* bestMove, fendoterSettings* settings);
int alphaBeta(field_t* board, int depth, int alpha, int beta, int p, move_t* bestMove);

/* board operations */
// Note: the do not check if the move is legal
void placePawn(char x, char y, char player, field_t* board){
    char pawn, pawnDataOffset, nextTurn;
    field_t* pawnMetaData;
    if (player == 1){
        pawn = PLAYER1PAWN;
        pawnDataOffset = PAWNS1NUM;
        nextTurn = 2;
    }
    else {
        pawn = PLAYER2PAWN;
        pawnDataOffset = PAWNS2NUM;
        nextTurn = 1;
    }
    field_t* field = board + x + 7*y;
    *field = *field | pawn;

    /* update meta data */
    pawnMetaData = board + pawnDataOffset;
    *pawnMetaData += 1;
    board[TURN] = nextTurn;
}

/* Note wallDirection is already the correct mask*/
void placeWall(char x, char y, char wallDirection, field_t* board){
    field_t *field, *field2;
    field = board + x + 7*y;
    *field = *field | wallDirection | HASWALL;
    switch (wallDirection){
        case WALLNORTH:
            field2 = field - 7;
            *field2 = *field2 | WALLSOUTH | HASWALL;
            break;
        case WALLSOUTH:
            field2 = field + 7;
            *field2 = *field2 | WALLNORTH | HASWALL;
            break;
        case WALLEAST:
            field2 = field + 1;
            *field2 = *field2 | WALLWEST | HASWALL;
            break;
        case WALLWEST:
            field2 = field - 1;
            *field2 = *field2 | WALLEAST | HASWALL;
            break;
    }
    
    /* update meta data */
    board[TURN] = (board[TURN] == 1) ? 2 : 1;
}

void movePawn(char x, char y, char u, char v, char player, field_t* board){
    field_t *startField, *endField;
    char pawn = (player == 1) ? PLAYER1PAWN : PLAYER2PAWN;

    startField = board + x + 7*y;
    endField = board + u + 7*v;
    // Remove pawn from original field
    *startField = *startField & ~OCCUPIED;

    // Add pawn to original field
    *endField = *endField | pawn;
}


move_t* makeMove(field_t* boardState, fendoterSettings* settings){
    printf("Making move\n");
    move_t* move = (move_t*) malloc(sizeof(move_t));
    for (int i = 0; i < 54; i++){
        printf("%x ", boardState[i]);
        if (i % 7 == 6){
            printf("\n");
        }
    }
    evaluateMoves(move, boardState, settings);
    return move;
}

void freeBestMove(move_t* bestMove){
    free(bestMove);
}

void evaluateMoves(move_t* bestMove, field_t* boardState, fendoterSettings* settings){
    switch (settings->playingMethod){
        case RANDOM:
            printf("Using playing method: RANDOM\n");
            playRandom(boardState, bestMove);
            printf("Total Nodes: %zu\n", totalNodes);
            printf("Number of nodes at each depth: %zu, %zu, %zu, %zu\n", depthNodes[0], depthNodes[1], depthNodes[2], depthNodes[3]);
            break;
        case MINIMAX:
            printf("Using playing method: MINIMAX\n");
            minimax(bestMove);
            break;
        case NEGAMAX:
            printf("Using playing method: NEGAMAX\n");
            negamax(boardState, settings->searchDepth, 1, bestMove, settings);
            printf("Number of nodes at each depth: %zu, %zu, %zu, %zu\n", depthNodes[0], depthNodes[1], depthNodes[2], depthNodes[3]);
            break;
        case ALPHABETA:
            printf("Using playing method: ALPHABETA\n");
            alphaBeta(boardState, settings->searchDepth, INT_MIN, INT_MAX, 1, bestMove);
            break;
    }
}


void calculateMoves(field_t* board, dynamic_array_move_t* moves, dynamic_array_ucharp* newBoards){
    char turn = (char) *(board + TURN);
    char curPlayer, curOpponent;
    char x, y, u, v;
    field_t *iField, *kField;

    if (turn == 1){
        curPlayer = PLAYER1PAWN;
        curOpponent = PLAYER2PAWN;
    }
    else {
        curPlayer = PLAYER2PAWN;
        curOpponent = PLAYER1PAWN;
    }

    for (int i = 0; i < 49; i++){
        iField = board + i;
        if ( (*iField & ASSIGNED) || (*iField & curOpponent) ){
            continue;
        }
        if (*iField & curPlayer){
            x = i % 7;
            y = i / 7;
            for (int j = 0; j < 4; j++){
                if (checkWallPlace(x, y, DIRECTIONS[j], board)){
                    field_t* newBoard = (field_t*) malloc(sizeof(field_t) * 54);
                    memcpy(newBoard, board, sizeof(field_t) * 54);
                    placeWall(x, y, DIRECTIONS[j], newBoard);
                    if (checkOpenArea(x, y, DIRECTIONS[j], newBoard)){
                        move_t* move = (move_t*) malloc(sizeof(move_t));
                        addItemUCharP(newBoards, newBoard);
                        move->moveType = PLACEWALL;
                        move->direction = DIRECTIONS[j];
                        move->x = x;
                        move->y = y;
                        move->u = -1;
                        move->v = -1;
                        move->player = turn;
                        addItemMove(moves, move);
                        totalNodes++;
                        continue;
                    }
                    else {
                        free(newBoard);
                    }
                }
            }
            for (int k = 0; k < 49; k++){
                kField = board + k;
                if ( (*kField & ASSIGNED) || (*kField & OCCUPIED) ){
                    continue;
                }
                u = k % 7;
                v = k / 7;
                if (checkPawnMove(x, y, u, v, board)){
                    field_t tempBoard[54];
                    memcpy(tempBoard, board, sizeof(field_t) * 54);
                    movePawn(x, y, u, v, turn, tempBoard);
                    for (int l = 0; l < 4; l++){
                        if (checkWallPlace(u, v, DIRECTIONS[l], tempBoard)){
                            field_t* newBoard = (field_t*) malloc(sizeof(field_t) * 54);
                            memcpy(newBoard, tempBoard, sizeof(field_t) * 54);
                            placeWall(u, v, DIRECTIONS[l], newBoard);
                            if (checkOpenArea(u, v, DIRECTIONS[l], newBoard)){
                                move_t* move = (move_t*) malloc(sizeof(move_t));
                                addItemUCharP(newBoards, newBoard);
                                move->moveType = MOVEPAWNANDWALL;
                                move->direction = DIRECTIONS[l];
                                move->x = x;
                                move->y = y;
                                move->u = u;
                                move->v = v;
                                move->player = turn;
                                addItemMove(moves, move);
                                totalNodes++;
                            }
                            else {
                                free(newBoard);
                            }
                        }
                    }
                }
            }
        }
        else { /* should only be called when field is empty !(*iField & OCCUPIED) */
            u = i % 7;
            v = i / 7;
            if (checkPawnPlace(u, v, turn, board)){
                field_t* newBoard = (field_t*) malloc(sizeof(field_t) * 54);
                move_t* move = (move_t*) malloc(sizeof(move_t));
                memcpy(newBoard, board, sizeof(field_t) * 54);
                placePawn(u, v, turn, newBoard);
                addItemUCharP(newBoards, newBoard);
                move->moveType = PLACEPAWN;
                move->x = -1;
                move->y = -1;
                move->u = u;
                move->v = v;
                move->player = turn;
                addItemMove(moves, move);
                totalNodes++;
            }
        }
    }
}


int checkRightField(int i, field_t* field, char player){
    if (i % 7 == 6){ /* Check for right boarder */
        return -1;
    }
    else if (*field & WALLEAST) { /* Check for wall before occupied */
        return 3;
    }
    else if (*(field + 1) & OCCUPIED) {
        if (*(field + 1) & player) {
            return 1;
        }
        else { /* If neighboring field not occupied by own player that it must be opponent's player */
            return 2;
        }
    }
    else {
        return 0;
    }
}


int checkLeftField(int i, field_t* field, char player){
    if (i % 7 == 0){ /* Check for left boarder */
        return -1;
    }
    else if (*field & WALLWEST) { /* Check for wall before occupied */
        return 3;
    }
    else if (*(field - 1) & OCCUPIED) {
        if (*(field - 1) & player) {
            return 1;
        }
        else { /* If neighboring field not occupied by own player that it must be opponent's player */
            return 2;
        }
    }
    else {
        return 0;
    }
}


int checkTopField(int i, field_t* field, char player){
    if (i < 7){ /* Check for top boarder */
        return -1;
    }
    else if (*field & WALLNORTH) { /* Check for wall before occupied */
        return 3;
    }
    else if (*(field - 7) & OCCUPIED) {
        if (*(field - 7) & player) {
            return 1;
        }
        else { /* If neighboring field not occupied by own player that it must be opponent's player */
            return 2;
        }
    }
    else {
        return 0;
    }
}


int checkBottomField(int i, field_t* field, char player){
    if (i > 41){ /* Check for bottom boarder */
        return -1;
    }
    else if (*field & WALLSOUTH) { /* Check for wall before occupied */
        return 3;
    }
    else if (*(field + 7) & OCCUPIED) {
        if (*(field + 7) & player) {
            return 1;
        }
        else { /* If neighboring field not occupied by own player that it must be opponent's player */
            return 2;
        }
    }
    else {
        return 0;
    }
}


int evaluateBoard(field_t* board){
    int grade = 0, areaGrade = 0, freedomGrade = 0;
    int freedomGradeCurPly = 0, freedomGradeOppPly = 0;
    field_t iField;

    char currentPlayer, opponentPlayer;
    char playerAssignedFields, opponentAssignedFields;

    /* Identify current player */
    char currentTurn = (char) *(board + TURN);
    if (currentTurn == 1){
        currentPlayer = PLAYER1PAWN;
        opponentPlayer = PLAYER2PAWN;
        playerAssignedFields = (char) *(board + ASSIGNEDFIELDS1);
        opponentAssignedFields = (char) *(board + ASSIGNEDFIELDS2);
    }
    else {
        currentPlayer = PLAYER2PAWN;
        opponentPlayer = PLAYER1PAWN;
        playerAssignedFields = (char) *(board + ASSIGNEDFIELDS2);
        opponentAssignedFields = (char) *(board + ASSIGNEDFIELDS1);
    }

    /* Check if current player has won */
    if (playerAssignedFields >= 25){
        return INT_MAX;
    }
    if (opponentAssignedFields >= 25){
        return INT_MIN;
    }

    /* Grade occupied area */
    areaGrade = playerAssignedFields - opponentAssignedFields;

    /* Grade freedom of the pawns */
    
    for (int i = 0; i < 49; i++){
        iField = *(board + i);
        if (iField & currentPlayer){
            switch (checkRightField(i, &iField, currentPlayer)) {
                case -1: /* Boarder to right */
                    freedomGradeCurPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeCurPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeCurPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeCurPly -= 6;
                    break;
                case 3: /* Wall */
                    freedomGradeCurPly -= 10;
                    break;
            }
            switch (checkLeftField(i, &iField, currentPlayer)){
                case -1: /* Boarder to left */
                    freedomGradeCurPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeCurPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeCurPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeCurPly -= 6;
                    break;
            }
            switch (checkTopField(i, &iField, currentPlayer)){
                case -1: /* Boarder to top */
                    freedomGradeCurPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeCurPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeCurPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeCurPly -= 6;
                    break;
            }
            switch (checkBottomField(i, &iField, currentPlayer)){
                case -1: /* Boarder to bottom */
                    freedomGradeCurPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeCurPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeCurPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeCurPly -= 6;
                    break;
            }
        }
        if (iField & opponentPlayer){
            switch (checkRightField(i, &iField, currentPlayer)) {
                case -1: /* Boarder to right */
                    freedomGradeOppPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeOppPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeOppPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeOppPly -= 6;
                    break;
                case 3: /* Wall */
                	freedomGradeOppPly -= 10;
                    break;
            }
            switch (checkLeftField(i, &iField, currentPlayer)){
                case -1: /* Boarder to left */
                    freedomGradeOppPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeOppPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeOppPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeOppPly -= 6;
                    break;
            }
            switch (checkTopField(i, &iField, currentPlayer)){
                case -1: /* Boarder to top */
                    freedomGradeOppPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeOppPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeOppPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeOppPly -= 6;
                    break;
            }
            switch (checkBottomField(i, &iField, currentPlayer)){
                case -1: /* Boarder to bottom */
                    freedomGradeOppPly -= 10;
                    break;
                case 0: /* Empty Field */
                    //freedomGradeOppPly += 1;
                    break;
                case 1: /* Occupied by own pawn */
                    freedomGradeOppPly -= 3;
                    break;
                case 2: /* Occupied by enemy pawn */
                    freedomGradeOppPly -= 6;
                    break;
            }
        }
    }

    freedomGrade = freedomGradeCurPly - freedomGradeOppPly;

    grade = areaGrade + freedomGrade; /* add coefficiants */
    return grade;
}

void playRandom(field_t* board, move_t* bestMove) {
    dynamic_array_move_t* moves;
    dynamic_array_ucharp* newBoards;
    arrayInitMove(&moves);
    arrayInitUCharP(&newBoards);

    srand(time(NULL)); // Seed the random number generator
    calculateMoves(board, moves, newBoards);
    printf("Number of moves: %zu\n", moves->size); // todo: size not correct for "standard move" check that calculate moves works as intended
    size_t placePawnMoves = 0;
    size_t placeWallMoves = 0;
    size_t movePawnAndWallMoves = 0;
    size_t undefinedMoves = 0;
    for (size_t i = 0; i < moves->size; i++) {
        move_t* tempMove = getItemMove(moves, i);
        switch (tempMove->moveType) {
            case PLACEPAWN:
                placePawnMoves++;
                break;
            case PLACEWALL:
                placeWallMoves++;
                break;
            case MOVEPAWNANDWALL:
                movePawnAndWallMoves++;
                break;
            default:
                undefinedMoves++;
                break;
            
        }
    }
    printf("Number of place pawn moves: %zu\n", placePawnMoves);
    printf("Number of place wall moves: %zu\n", placeWallMoves);
    printf("Number of move pawn and wall moves: %zu\n", movePawnAndWallMoves);
    printf("Number of undefined moves: %zu\n", undefinedMoves);
    if (newBoards->size > 0) {
        size_t randomIndex = rand() % newBoards->size;
        move_t* randomMove = getItemMove(moves, randomIndex);
        bestMove->moveType = randomMove->moveType;
        bestMove->x = randomMove->x;
        bestMove->y = randomMove->y;
        bestMove->u = randomMove->u;
        bestMove->v = randomMove->v;
        bestMove->direction = randomMove->direction;
        bestMove->player = randomMove->player;
        printf("Random move is:\n");
        printf("Move type: %x\n", bestMove->moveType);
        printf("x: %d\n", bestMove->x);
        printf("y: %d\n", bestMove->y);
        printf("u: %d\n", bestMove->u);
        printf("v: %d\n", bestMove->v);
        printf("direction: %d\n", bestMove->direction);
        printf("player: %d\n", bestMove->player);
    }
    freeArrayMove(moves);
    freeArrayUCharP(newBoards);
}

int negamax(field_t* board, int depth, int p, move_t* bestMove, fendoterSettings* settings){
    int grade, maxEval, eval;
    dynamic_array_move_t* moves;
    dynamic_array_ucharp* newBoards;
    arrayInitMove(&moves);
    arrayInitUCharP(&newBoards);

    if (depth == 0) {
        grade = p * evaluateBoard(board);
        return grade;
    }

    maxEval = INT_MIN;
    calculateMoves(board, moves, newBoards); // each depth produces the factor of around 200 new boards 186-37856-7618193
    depthNodes[settings->searchDepth - depth] += newBoards->size;

    for (size_t i = 0; i < newBoards->size; i++) {
        eval = -negamax(newBoards->array[i], depth - 1, -p, bestMove, settings);
        if (eval > maxEval) {
            maxEval = eval;
            if (depth == settings->searchDepth){ // override bestMove only in the top most layer
                move_t* tempMove = getItemMove(moves, i);
                bestMove->moveType = tempMove->moveType;
                bestMove->x = tempMove->x;
                bestMove->y = tempMove->y;
                bestMove->u = tempMove->u;
                bestMove->v = tempMove->v;
                bestMove->direction = tempMove->direction;
                bestMove->player = tempMove->player;
                printf("Best move with grade %d is:\n", maxEval);
                printf("Move type: %x\n", bestMove->moveType);
                printf("x: %d\n", bestMove->x);
                printf("y: %d\n", bestMove->y);
                printf("u: %d\n", bestMove->u);
                printf("v: %d\n", bestMove->v);
                printf("direction: %d\n", bestMove->direction);
                printf("player: %d\n", bestMove->player);
            }
        }
    }
    freeArrayMove(moves);
    freeArrayUCharP(newBoards);
    return maxEval;
}


int minimax(move_t* bestMove){
    return 1;
}

int alphaBeta(field_t* board, int depth, int alpha, int beta, int p, move_t* bestMove){
    return 1;
}

// Board representation in cpp?
/*
- array of 53 uint8_t 49 for the fields and 4 for num of pawns1/2, num of assigned fields1/2


- array for moves, append at end









*/





// Rules in cpp (as functions -> rules.cpp)