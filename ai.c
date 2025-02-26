#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "dynamicarray.c"
#include "gamerep.h"
#include "rules.c"


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
            break;
        case MINIMAX:
            printf("Using playing method: MINIMAX\n");
            minimax(bestMove);
            break;
        case NEGAMAX:
            printf("Using playing method: NEGAMAX\n");
            negamax(boardState, settings->searchDepth, 1, bestMove, settings);
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
    char wallDirections[4] = {WALLNORTH, WALLSOUTH, WALLEAST, WALLWEST};
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
                if (checkWallPlace(x, y, wallDirections[j], board)){
                    field_t* newBoard = (field_t*) malloc(sizeof(field_t) * 54);
                    move_t* move = (move_t*) malloc(sizeof(move_t));
                    memcpy(newBoard, board, sizeof(field_t) * 54);
                    placeWall(x, y, wallDirections[j], newBoard);
                    addItemUCharP(newBoards, newBoard);
                    move->moveType = PLACEWALL;
                    move->direction = wallDirections[j];
                    move->x = x;
                    move->y = y;
                    move->u = -1;
                    move->v = -1;
                    move->player = turn;
                    addItemMove(moves, move);
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
                        if (checkWallPlace(u, v, wallDirections[l], tempBoard)){
                            field_t* newBoard = (field_t*) malloc(sizeof(field_t) * 54);
                            move_t* move = (move_t*) malloc(sizeof(move_t));
                            memcpy(newBoard, tempBoard, sizeof(field_t) * 54);
                            placeWall(u, v, wallDirections[l], newBoard);
                            addItemUCharP(newBoards, newBoard);
                            move->moveType = MOVEPAWNANDWALL;
                            move->direction = wallDirections[l];
                            move->x = x;
                            move->y = y;
                            move->u = u;
                            move->v = v;
                            move->player = turn;
                            addItemMove(moves, move);
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
            }
        }
    }
}


int evaluateBoard(field_t* board){
    int grade, areaGrade, freedomGrade;
    int freedomGradeCurPly, freedomGradeOppPly;
    field_t iField;

    char wallDirections[4] = {WALLNORTH, WALLSOUTH, WALLEAST, WALLWEST};
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
            for(int d = 0; d < 4; d++){
                if (iField & wallDirections[d]){
                    freedomGradeCurPly -= 1;
                }
                /*else if (check neighboring fields for enemy and own pawns){
                    
                }*/
                /*else if (check if field is next to boarder) {
                }*/
            }
        }
        if (iField & opponentPlayer){
            for(int d = 0; d < 4; d++){
                if (iField & wallDirections[d]){
                    freedomGradeOppPly -= 1;
                }
                /*else if (check neighboring fields for enemy and own pawns){
                    
                }*/
                /*else if (check if field is next to boarder) {
                }*/
            }
        }
    }

    grade = areaGrade + freedomGrade; /* add coefficiants */
    return grade;

/*    # grade movement freedom/
    /*
        # grade movement freedom
        # freedom_grade = self.calculateMoves(board)[0] # prossessing time too long
        freedom_grade, current_player_freedom_grade, opponent_freedom_grade = 0, 0, 0
        for direction in ["N", "E", "S", "W"]: # estimate freedom by checking walls/pawns/boarders next to pawns
            for pawn in current_pawns:
                if (pawn.getCoordinates()[0] == 0 and direction == "W") or (pawn.getCoordinates()[0] == board.getSize() - 1 and direction == "E") or (pawn.getCoordinates()[1] == 0 and direction == "N") or (pawn.getCoordinates()[1] == board.getSize() - 1 and direction == "S"):
                    current_player_freedom_grade -=1
                elif board.getFields()[pawn.getCoordinates()].getWall(direction):
                    current_player_freedom_grade -= 1
                else:
                    end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                    if end_coords:
                        if board.getField(end_coords).getPawn():
                            current_player_freedom_grade -= PAWN_BARRIER_COEF*1
                # different approach (but more computing heavy):
                #end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                #if end_coords:
                #    if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                #        current_player_freedom_grade += 1
            for pawn in opponent_pawns:
                if (pawn.getCoordinates()[0] == 0 and direction == "W") or (pawn.getCoordinates()[0] == board.getSize() - 1 and direction == "E") or (pawn.getCoordinates()[1] == 0 and direction == "N") or (pawn.getCoordinates()[1] == board.getSize() - 1 and direction == "S"):
                    opponent_freedom_grade -=1
                elif board.getFields()[pawn.getCoordinates()].getWall(direction):
                    opponent_freedom_grade -= 1
                else:
                    end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                    if end_coords:
                        if board.getField(end_coords).getPawn():
                            opponent_freedom_grade -= PAWN_BARRIER_COEF*1
                # different approach (but more computing heavy):
                # end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                # if end_coords:
                #     if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                #         opponent_freedom_grade += 1

        freedom_grade = (current_player_freedom_grade / len(current_pawns)) - (opponent_freedom_grade / len(opponent_pawns))
        
        grade = AREA_COEF * area_grade + FREEMOV_COEF * freedom_grade
        return grade*/
    return 1;
}

void playRandom(field_t* board, move_t* bestMove) {
    dynamic_array_move_t* moves;
    dynamic_array_ucharp* newBoards;
    arrayInitMove(&moves);
    arrayInitUCharP(&newBoards);

    srand(time(NULL)); // Seed the random number generator
    calculateMoves(board, moves, newBoards);
    printf("Number of moves: %d\n", moves->size); // todo: size not correct for "standard move" check that calculate moves works as intended
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
    calculateMoves(board, moves, newBoards);

    for (size_t i = 0; i < newBoards->size; i++) {
        eval = -negamax(newBoards->array[i], depth - 1, -p, bestMove, settings);
        if (eval > maxEval) {
            maxEval = eval;
            if (depth == settings->searchDepth){ // override bestMove only in the top most layer
                memcpy(bestMove, moves->array[i], sizeof(move_t));
                move_t* tempMove = getItemMove(moves, i);
                bestMove->moveType = tempMove->moveType;
                bestMove->x = tempMove->x;
                bestMove->y = tempMove->y;
                bestMove->u = tempMove->u;
                bestMove->v = tempMove->v;
                bestMove->direction = tempMove->direction;
                bestMove->player = tempMove->player;
                printf("Best move is:\n");
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