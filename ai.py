import random, copy

from board import Board, Field, Pawn
from moves import Move, PlacePawn, MovePawnAndWall, PlaceWall, MovePawn
from rules import Referee


AREA_COEF = 1
FREEMOV_COEF = 0.05


class Fendoter():
    
    def __init__(self, player, grading_method: str) -> None:
        self.ref = Referee()
        self.player = player
        self.opponent = 3 - player #TODO: hardcoded, only works for 2 player
        self.grading_method = grading_method
    
    def makeMove(self, board: Board) -> Move:
        possible_moves, new_boards = self.calculateMoves(board)
        best_move: Move = self.evaluateMoves(new_boards, possible_moves, self.grading_method)
        return best_move
    
    def calculateMoves(self, board: Board):
        own_pawns: list[Pawn] = board.getPawns(self.player)
        fields: list[Field] = board.getFieldsFlat()
        board_state: dict = copy.deepcopy(board.getState())

        moves = []
        new_boards = []
        for pawn in own_pawns:
            for field in fields:
                # Place new Pawn
                if self.ref.checkLegalMove(PlacePawn(field.getCoordinates(), self.player), board_state):
                    moves.append(PlacePawn(field.getCoordinates(), self.player))
                    new_board = Board(board_state['size'], board_state['max_pawns'])
                    new_board.loadState(copy.deepcopy(board_state))
                    new_board.placePawn(field.getCoordinates(), self.player)
                    new_boards.append(new_board)
                for direction in ["N", "E", "S", "W"]:
                    # Move Pawn and place Wall
                    if self.ref.checkLegalMove(MovePawnAndWall(pawn.getPosition(), field.getCoordinates(), direction, self.player), board_state):
                        moves.append(MovePawnAndWall(pawn.getPosition(), field.getCoordinates(), direction, self.player))
                        new_board = Board(board_state['size'], board_state['max_pawns'])
                        new_board.loadState(copy.deepcopy(board_state))
                        new_board.movePawn(pawn.getPosition(), field.getCoordinates())
                        new_board.placeWall(field.getCoordinates(), direction, self.player)
                        new_boards.append(new_board)
                    # Place Wall without moving Pawn
                    if self.ref.checkLegalMove(PlaceWall(field.getCoordinates(), direction, self.player), board_state):
                        moves.append(PlaceWall(field.getCoordinates(), direction, self.player))
                        new_board = Board(board_state['size'], board_state['max_pawns'])
                        new_board.loadState(copy.deepcopy(board_state))
                        new_board.placeWall(field.getCoordinates(), direction, self.player)
                        new_boards.append(new_board)
                        
        return moves, new_boards
    
    #TODO: not needed anymore
    def simulateMove(self, move: Move, board_state: dict) -> dict:
        new_board_state = board_state.copy()
        new_board_state['moves_list'].append(move)
        match move:
            case PlacePawn():
                new_board_state['fields'][move.coordinates].addPawn(Pawn(move.player))
            case PlaceWall():
                new_board_state['fields'][move.coordinates].placeWall(move.direction)
                if move.direction == 'N' and move.coordinates[1] != 0:
                    new_board_state['fields'][move.coordinates[0], move.coordinates[1] - 1].placeWall('S')
                elif move.direction == 'E' and move.coordinates[0] != self.size - 1:
                    new_board_state['fields'][move.coordinates[0] + 1, move.coordinates[1]].placeWall('W')
                elif move.direction == 'S' and move.coordinates[1] != self.size - 1:
                    new_board_state['fields'][move.coordinates[0], move.coordinates[1] + 1].placeWall('N')
                elif move.direction == 'W' and move.coordinates[0] != 0:
                    new_board_state['fields'][move.coordinates[0] - 1, move.coordinates[1]].placeWall('E')
            case MovePawn():
                new_board_state['fields'][move.start_coordinates].removePawn()
                new_board_state['fields'][move.end_coordinates].addPawn(Pawn(move.player))
            case MovePawnAndWall():
                new_board_state = self.simulateMove(MovePawn(move.start_coordinates, move.end_coordinates, move.player), new_board_state)
                new_board_state = self.simulateMove(PlaceWall(move.end_coordinates, move.direction, move.player), new_board_state)
        return new_board_state
    
    def evaluateMoves(self, new_boards: list[Board], possible_moves: list[Move], method: str) -> Move:
        match method:
            case "depth1":
                return self.depth1Eval(new_boards)
            case "random":
                return self.randomGrading(possible_moves)
            case "minimax":
                ...
                #grading_function = self.minimaxGrading #TODO: look up what this is
            case "alpha-beta":
                ...
                #grading_function = self.alphaBetaGrading #TODO: look up what this is
            case _:
                raise ValueError("Invalid grading method")
    
    
    def randomGrading(self, moves: list[Move]) -> int:
        return random.choice(moves)

    def depth1Eval(self, boards: list[Board]):
        best_move = boards[0]
        best_grade = self.depth1Grading(best_move)
        for state in boards:
            grade = self.depth1Grading(state)
            if grade > best_grade:
                best_move = state
                best_grade = grade
        return best_move
    
    def depth1Grading(self, board: Board) -> int:
        grade = 0
        # grade area
        grade += AREA_COEF*(board.getPlayerArea(self.player) - board.getPlayerArea(self.opponent))
        # grade movement freedom
        grade += FREEMOV_COEF*len(self.calculateMoves(board)[0])
        return grade
    
        