#include <stdlib.h>

#include "gamerep.h"

class Fendoter {
    private:
        unsigned int search_depth = 0;
        int playingMethod = 0;
        field_t boardState[54] = {0}; //49 fields + 2 bytes num of pawns1/2 + 2 bytes num of assigned fields1/2 + 1 byte turn
    public:
        Fendoter();
        ~Fendoter();
        int makeMove(int state);
        void evaluateMoves(move_t* bestMove);
        int playRandom(move_t* bestMove);
        int minimax(move_t* bestMove);
        int negamax(field_t* board, int depth, int p, move_t* bestMove);
        int alphabeta(field_t* board, int depth, int alpha, int beta, int p, move_t* bestMove);
};

void convertBoardState(int* state, field_t* board);
void calculateMoves(field_t* board);