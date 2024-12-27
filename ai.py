from board import Board, Field, Pawn
from moves import Move, PlacePawn, MovePawnAndWall, PlaceWall, MovePawn
from rules import Referee

class Fendoter():
    
    def __init__(self, player, grading_method: str) -> None:
        self.ref = Referee()
        self.player = player
        match grading_method:
            case "depth1":
                self.grading_function = self.depth1Grading
            case "random":
                self.grading_function = self.randomGrading
            case "minimax":
                self.grading_function = self.minimaxGrading #TODO: look up what this is
            case "alpha-beta":
                self.grading_function = self.alphaBetaGrading #TODO: look up what this is
            case _:
                raise ValueError("Invalid grading method")
    
    def nextMove(self, board_state: dict) -> Move:
        possible_moves, new_board_states: tuple[list[Move],list[dict]] = self.calculateMoves(board_state)
        best_move: Move = self.evaluateMoves(possible_moves, self.grading_function)
        return best_move
    
    def calculateMoves(self, board_state: dict) -> list[Move]:
        match self.player:
            case 1:
                own_pawns = board_state['pawns1']
            case 2:
                own_pawns = board_state['pawns2']
            case _:
                raise ValueError("Invalid player")
        fields = board_state['fields']

        moves = []
        new_board_states = []
        for pawn in own_pawns:
            for field in fields:
                # Place new Pawn
                if self.ref.checkLegalMove(PlacePawn(field, self.player), board_state):
                    moves.append(PlacePawn(field, self.player))
                    new_board_states.append(self.simulateMove(PlacePawn(field, self.player), board_state))
                for direction in ["N", "E", "S", "W"]:
                    # Move Pawn and place Wall
                    if self.ref.checkLegalMove(MovePawnAndWall(pawn.getPosition(), field, direction, self.player), board_state):
                        moves.append(MovePawnAndWall(pawn.getPosition(), field, direction, self.player))
                        new_board_states.append(self.simulateMove(MovePawnAndWall(pawn.getPosition(), field, direction, self.player), board_state))
                    # Place Wall without moving Pawn
                    if self.ref.checkLegalMove(PlaceWall(field.getCoordinates(), direction, self.player), board_state):
                        moves.append(PlaceWall(field, direction, self.player))
                        new_board_states.append(self.simulateMove(PlaceWall(field.getCoordinates(), direction, self.player), board_state))
                        
        return moves, new_board_states
    
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
    
    def evaluateMoves(self, board_states: list[list[Field]], grading_function: callable) -> Move:
        best_move = board_states[0]
        best_grade = grading_function(best_move)
        for state in board_states:
            grade = grading_function(state)
            if grade > best_grade:
                best_move = state
                best_grade = grade
        return best_move
    
    def depth1Grading(self, state: list[Field]) -> int:
        grade = 0
        for field in state:
            