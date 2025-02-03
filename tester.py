import random
from timeit import timeit
import cProfile

from board import Board, Field, Pawn
from ai import Fendoter
from rules import Referee
from moves import PlacePawn, MovePawn, MovePawnAndWall, PlaceWall
from handler import board2Array


def generateBoard() -> Board:
    board_size = 7
    max_pawns = 7
    board = Board(board_size, max_pawns, new=True)
    # remove start pawns
    board.removePawn((0, 3))
    board.removePawn((6, 3))
    random_turn = random.randint(1, 2)
    board.setTurn(random_turn)
    
    # in percent
    wall_chance = 10
    pawn_wall_chance = 8
    pawn_chance = 5
    for field in board.getFieldsFlat():
        random_number = random.randint(1, 100)
        if random_number <= wall_chance:
            random_direction = random.choice(["N", "E", "S", "W"])
            board.placeWall(field.getCoordinates(), random_direction, 1) # player index is irrelevant
        elif random_number <= (wall_chance + pawn_wall_chance):
            random_direction = random.choice(["N", "E", "S", "W"])
            player_index = random.randint(1, 2)
            board.placeWall(field.getCoordinates(), random_direction, player_index)
            board.placePawn(field.getCoordinates(), player_index)
        elif random_number <= (wall_chance + pawn_chance):        
            player_index = random.randint(1, 2)
            board.placePawn(field.getCoordinates(), player_index)
    return board


def checkPerformance(test_func: str, board: Board, number: int = 1) -> float:
    match test_func:
        case 'makeMove':
            #execution_time = timeit(lambda: fendoter.makeMove(board), number=number)
            execution_time = 0
            cProfile.runctx("fendoter.makeMove(board)", globals(), locals(), sort='tottime')
        case 'calculateMoves':
            #execution_time = timeit(lambda: fendoter.calculateMoves(board), number=number)
            execution_time = 0
            cProfile.runctx("fendoter.calculateMoves(board)", globals(), locals(), sort='tottime')
        case 'evaluateFields':
            #execution_time = timeit(lambda: board.evaluateFields, number=number)
            execution_time = 0
            cProfile.runctx("board.evaluateFields", globals(), locals(), sort='tottime')
        case 'gradingII':
            #execution_time = timeit(lambda: fendoter.gradingII(board), number=number)
            execution_time = 0
            cProfile.runctx("fendoter.gradingII(board)", globals(), locals(), sort='tottime')
        case 'legalPlacePawn':
            coords = random.choice(board.getFieldsFlat()).getCoordinates()
            player = random.randint(1, 2)
            execution_time = timeit(lambda: ref.checkLegalMove(PlacePawn(coords, player), board.getTurn(), board.getState()), number=number)
        case 'legalMovePawn':
            start_coords = random.choice(board.getFieldsFlat()).getCoordinates()
            end_coords = random.choice(board.getFieldsFlat()).getCoordinates()
            player = random.randint(1, 2)
            execution_time = timeit(lambda: ref.checkLegalMove(MovePawn(start_coords, end_coords, player), board.getTurn(), board.getState()), number=number)
        case 'legalMovePawnAndWall':
            start_coords = random.choice(board.getFieldsFlat()).getCoordinates()
            end_coords = random.choice(board.getFieldsFlat()).getCoordinates()
            player = random.randint(1, 2)
            direction = random.choice(["N", "E", "S", "W"])
            execution_time = timeit(lambda: ref.checkLegalMove(MovePawnAndWall(start_coords, end_coords, direction, player), board.getTurn(), board.getState()), number=number)
        case _:
            raise ValueError("Invalid test function")
        
    return execution_time

def checkLoadBoard(board: Board) -> None:
    print("Original board:")
    print(board)
    own_pawns: list[Pawn] = board.getPawns(board.getTurn())
    fields: list[Field] = board.getFieldsFlat()
    board_state = board.getState()
    
    ref = Referee()
    place_pawn_flag = True
    move_pawn_flag = True
    place_wall_flag = True    
    
    for pawn in own_pawns:
        for field in fields:
            if place_pawn_flag and ref.checkLegalMove(PlacePawn(field.getCoordinates(), board.getTurn()), board_state):
                place_pawn_flag = False
                new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                #new_board.loadState(copy.deepcopy(board_state))
                new_board.loadState(board_state)
                new_board.placePawn(field.getCoordinates(), board.getTurn())
                new_board.endTurn()
                print("Place Pawn:")
                print(new_board)
            if move_pawn_flag or place_wall_flag:
                for direction in ["N", "E", "S", "W"]:
                    if move_pawn_flag and ref.checkLegalMove(MovePawnAndWall(pawn.getCoordinates(), field.getCoordinates(), direction, board.getTurn()), board_state):
                        move_pawn_flag = False
                        new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                        #new_board.loadState(copy.deepcopy(board_state))
                        new_board.loadState(board_state)
                        new_board.movePawn(pawn.getCoordinates(), field.getCoordinates())
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        print("Move Pawn and Place Wall:")
                        print(new_board)
                    if place_wall_flag and ref.checkLegalMove(PlaceWall(field.getCoordinates(), direction, board.getTurn()), board_state):
                        place_wall_flag = False
                        new_board = Board(board_state['size'], board_state['max_pawns'], new=False)
                        #new_board.loadState(copy.deepcopy(board_state))
                        new_board.loadState(board_state)
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        print("Place Wall:")
                        print(new_board)
    

if __name__ == "__main__":
    timer = True
    test_func = "makeMove" # makeMove, calculateMoves, evaluateFields, gradingII, legalPlacePawn, legalMovePawn, legalMovePawnAndWall
    different_boards = 1
    repetitions = 1
    
    ref = Referee()
    
    ai_player = 1
    ai_brain = "alpha-beta"
    ai_search_depth = 3
    fendoter = Fendoter(ai_player, ai_brain, ai_search_depth)
    print("Performance test:")
    
    for _ in range(different_boards):
        #random_board = Board(7, 7, new=True)
        random_board = generateBoard()
        print(random_board)
        c_board = board2Array(random_board)
        if timer:
            execution_time = checkPerformance(test_func, random_board, repetitions)
        else:
            checkLoadBoard(random_board)
        # with open("performance_data.csv", "a") as file:
        #     board_str = random_board.__str__()
        #     #file.write(f"{board_str};{execution_time:.6f}\n")
        #     file.write(f"{execution_time:.6f}\n")
        # print(f"{test_func} took {execution_time:.6f} seconds")
    

