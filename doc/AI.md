# Fendoter

The `Fendoter` (Fendo + Roboter) class is a computer player for the fendo game.  

#### `__init__`  
Initializes a Fendoter object.
- player: int -> defines for which player Fendoter should play
- playing_method: str -> defines the search algorithm or other playstyle Fendoter should deploy  
(For the different styles implemented go to [evaluateMoves](#evaluatemoves))
- search_depth: int -> the max. search deapth to search the search tree of next moves

#### `makeMove`
Given a board returns the best move evaluated based on the given playing method.  
In debug mode the search tree is printed out.

#### `evaluateMoves`
Executed the corresponding playing method search algorithm or playstyle.  
Currently implemented play-styles are:
`depth1`  
...  
`random`  
Chooses a random legal move.  
`minimax`  
Deploys the minimax-algorithm  
`negamax`  
Deploys the negamax-algorithm  
`alpha-beta`  
Deploys the alpha-beta-(pruning) algorithm  

#### `calculateMoves`

#### `randomGrading`
rename to "random" and move calcualte moves into random

#### `grade`
grading function
- how it works
- what was done for performance
- what could be done: better coefficiants, other strategie methods
- complete function written out ($$equation$$)

#### `minimax`
short what it does (siehe tum pdf)
and how its deployed here

#### `negamax`
short what it does compared to minimax
and how its deployed here

#### `alphabeta`
short what is does compared to negamax
and how it is deployed here