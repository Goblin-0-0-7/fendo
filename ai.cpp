#include <stdlib.h>
#include <vector>

#include "ai.h"
#include "gamerep.h"
#include "rules.cpp"

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


int evaluateBoard(field_t* board){

}

void convertBoardState(int* state, field_t* board){

}

void calculateMoves(field_t* board, std::vector<move_t>* moves, std::vector<field_t*>* newBoards){
    char turn = (char) *(board + TURN);
    char curPlayer, curOpponent;
    char x, y, u, v;
    char directions[4] = {NORTH, EAST, SOUTH, WEST};
    field_t* iField;
    field_t newBoard[54];
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
                    newBoards->push_back(newBoard);
                    move.moveType = PLACEWALL;
                    move.direction = directions[j];
                    move.x = x;
                    move.y = y;
                    move.u = -1;
                    move.v = -1;
                    move.player = turn;
                    moves->push_back(move);
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
                            newBoards->push_back(newBoard);
                            move.moveType = MOVEPAWNANDWALL;
                            move.direction = directions[l];
                            move.x = x;
                            move.y = y;
                            move.u = u;
                            move.v = v;
                            move.player = turn;
                            moves->push_back(move);
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
                newBoards->push_back(newBoard);
                move.moveType = PLACEPAWN;
                move.x = -1;
                move.y = -1;
                move.u = u;
                move.v = v;
                move.player = turn;
                moves->push_back(move);
            }
        }
    }
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
Fendoter::Fendoter(){
}

Fendoter::~Fendoter(){
}

int Fendoter::makeMove(int state){
    move_t move;
    convertBoardState(&state, boardState);
    evaluateMoves(&move);
}

void Fendoter::evaluateMoves(move_t* bestMove){
    switch (playingMethod){
        case RANDOM:
            playRandom(bestMove);
            break;
        case MINIMAX:
            minimax(bestMove);
            break;
        case NEGAMAX:
            negamax(boardState, search_depth, 1, bestMove);
            break;
        case ALPHABETA:
            alphabeta(boardState, search_depth, '-inf', 'inf', 1, bestMove);
            break;
    }
}

int Fendoter::negamax(field_t* board, int depth, int p, move_t* bestMove){
    int grade, maxEval, eval;
    std::vector<move_t> moves;
    std::vector<field_t*> newBoards;

    if (depth == 0) {
        grade = p * evaluateBoard(board);
        return grade;
    }

    maxEval = p * INT_MAX;
    calculateMoves(board, &moves, &newBoards);

    for (size_t i = 0; i < newBoards.size(); i++) {
        eval = -negamax(newBoards[i], depth - 1, -p, bestMove);
        if (eval > maxEval) {
            maxEval = eval;
            if (depth == search_depth){ // override bestMove only in the top most layer
                *bestMove = moves[i];
            }
        }
    }
    return maxEval;
}


// Board representation in cpp?
/*
- array of 53 uint8_t 49 for the fields and 4 for num of pawns1/2, num of assigned fields1/2


- array for moves, append at end









*/





// Rules in cpp (as functions -> rules.cpp)