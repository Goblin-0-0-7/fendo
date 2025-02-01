/* Moves */
#define GAMESTART             0x1
#define GAMEEND               0xF
#define PLACEWALL             0x2
#define PLACEPAWN             0x4
#define MOVEPAWN              0x8
#define MOVEPAWNANDWALL       MOVEPAWN | PLACEWALL

/*                Fields                                    *\
|* Fields are represented by a 8-bit value                  *|
**  bit | description
**  ----+----------------
**  1,2 | occupation (00 = empty, 01 = player1, 10 = player2)
**   3  | any wall (1 = yes, 0 = no)
**   4  | wall north
**   5  | wall south
**   6  | wall east
**   7  | wall west
**   8  | closed space assigned to a player (1 = yes, 0 = no)
\*                                                          */
#define EMPTYFIELD            0x00
#define PLAYER1PAWN           0x01
#define PLAYER2PAWN           0x02
#define OCCUPIED              PLAYER1PAWN | PLAYER2PAWN
#define HASWALL               0x04
#define WALLNORTH             0x08
#define WALLSOUTH             0x10
#define WALLEAST              0x20
#define WALLWEST              0x40
#define ASSIGNED              0x80

/*                Directions                                *\
|* Directions are represented by a 4-bit value               *|
**  bit | description
**  ----+----------------
**  1  | north
**  2  | south
**  3  | east
**  4  | west
\*                                                          */
#define NORTH                 0x1
#define SOUTH                 0x2
#define EAST                  0x4
#define WEST                  0x8


typedef unsigned char field_t;