#include <stdlib.h>
#include <string.h>

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
    char pawn, pawnDataOffset;
    field_t* pawnMetaData;
    if (player == 1){
        pawn = PLAYER1PAWN;
        pawnDataOffset = PAWNS1NUM;
    }
    else {
        pawn = PLAYER2PAWN;
        pawnDataOffset = PAWNS2NUM;
    }
    field_t* field = board + x + 7*y;
    *field = *field | pawn;

    // update meta data
    pawnMetaData = board + pawnDataOffset;
    *pawnMetaData += 1;
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



/*
def calculateMoves(self, board: Board) -> tuple[list[Move], list[Board]]:
        # debug start
        #print("\nCurrent Board:\n")
        #print(board)
        # debug end
        
        own_pawns: list[Pawn] = board.getPawns(board.getTurn())
        fields: list[Field] = board.getFieldsFlat()
        board_state: dict = board.getState()

        moves = []
        new_boards = []
        for pawn in own_pawns:
            for field in fields:
                # Place new Pawn
                if self.ref.checkLegalMove(PlacePawn(field.getCoordinates(), board.getTurn()), board_state):
                    moves.append(PlacePawn(field.getCoordinates(), board.getTurn()))
                    new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                    #new_board.loadState(copy.deepcopy(board_state))
                    new_board.loadState(board_state)
                    new_board.placePawn(field.getCoordinates(), board.getTurn())
                    new_board.endTurn()
                    new_boards.append(new_board)
                for direction in ["N", "E", "S", "W"]:
                    # Move Pawn and place Wall
                    if self.ref.checkLegalMove(MovePawnAndWall(pawn.getCoordinates(), field.getCoordinates(), direction, board.getTurn()), board_state):
                        moves.append(MovePawnAndWall(pawn.getCoordinates(), field.getCoordinates(), direction, board.getTurn()))
                        new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                        #new_board.loadState(copy.deepcopy(board_state))
                        new_board.loadState(board_state)
                        new_board.movePawn(pawn.getCoordinates(), field.getCoordinates())
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        new_boards.append(new_board)
                    # Place Wall without moving Pawn
                    if self.ref.checkLegalMove(PlaceWall(field.getCoordinates(), direction, board.getTurn()), board_state):
                        moves.append(PlaceWall(field.getCoordinates(), direction, board.getTurn()))
                        new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                        #new_board.loadState(copy.deepcopy(board_state))
                        new_board.loadState(board_state)
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        new_boards.append(new_board)
                        
        return moves, new_boards
*/


//TODO: return should be move_t
move_t* makeMove(field_t* boardState, fendoterSettings* settings){
    printf("Making move\n");
    move_t* move;
    evaluateMoves(move, boardState, settings);
    return move;
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
    char directions[4] = {NORTH, EAST, SOUTH, WEST};
    field_t* iField;
    field_t newBoard[54]; //TODO: allocate mem on heap
    move_t move;

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
                if (checkWallPlace(x, y, directions[j], board)){
                    memcpy(newBoard, board, sizeof(field_t) * 54);
                    placeWall(x, y, directions[j], newBoard);
                    addItemUCharP(newBoards, newBoard);
                    move.moveType = PLACEWALL;
                    move.direction = directions[j];
                    move.x = x;
                    move.y = y;
                    move.u = -1;
                    move.v = -1;
                    move.player = turn;
                    addItemMove(moves, &move);
                }
            }
            for (int k = 0; k < 49; k++){
                if ( (*iField & ASSIGNED) || (*iField & OCCUPIED) ){
                    continue;
                }
                u = k % 7;
                v = k / 7;
                if (checkPawnMove(x, y, u, v, board)){
                    memcpy(newBoard, board, sizeof(field_t) * 54);
                    movePawn(x, y, u, v, turn, newBoard);
                    for (int l = 0; l < 4; l++){
                        if (checkWallPlace(u, v, directions[l], newBoard)){
                            placeWall(u, v, directions[l], newBoard);
                            addItemUCharP(newBoards, newBoard);
                            move.moveType = MOVEPAWNANDWALL;
                            move.direction = directions[l];
                            move.x = x;
                            move.y = y;
                            move.u = u;
                            move.v = v;
                            move.player = turn;
                            addItemMove(moves, &move);
                        }
                    }
                }
            }
        }
        else { /* should only be called when field is empty !(*iField & OCCUPIED) */
            u = i % 7;
            v = i / 7;
            if (checkPawnPlace(u, v, turn, board)){
                memcpy(newBoard, board, sizeof(field_t) * 54);
                placePawn(u, v, turn, board);
                addItemUCharP(newBoards, newBoard);
                move.moveType = PLACEPAWN;
                move.x = -1;
                move.y = -1;
                move.u = u;
                move.v = v;
                move.player = turn;
                addItemMove(moves, &move);
            }
        }
    }
}


int evaluateBoard(field_t* board){
    return 1;
}

void playRandom(field_t* board, move_t* bestMove) {
    dynamic_array_move_t* moves;
    dynamic_array_ucharp* newBoards;
    arrayInitMove(&moves);
    arrayInitUCharP(&newBoards);

    calculateMoves(board, moves, newBoards);
    printf("Number of moves: %d\n", moves->size);
    if (newBoards->size > 0) {
        size_t randomIndex = rand() % newBoards->size;
        memcpy(bestMove, moves->array[randomIndex], sizeof(move_t));
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

    maxEval = p * INT_MAX;
    calculateMoves(board, moves, newBoards);

    for (size_t i = 0; i < newBoards->size; i++) {
        eval = -negamax(newBoards->array[i], depth - 1, -p, bestMove, settings);
        if (eval > maxEval) {
            maxEval = eval;
            if (depth == settings->searchDepth){ // override bestMove only in the top most layer
                memcpy(bestMove, moves->array[i], sizeof(move_t));
            }
        }
    }
    //arrayFreeMove(&moves);
    //arrayFreeUCharP(&newBoards);
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