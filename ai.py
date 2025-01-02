import random, copy
from tqdm import tqdm

from board import Board, Field, Pawn
from moves import Move, PlacePawn, MovePawnAndWall, PlaceWall, MovePawn
from rules import Referee, findValidPath


AREA_COEF = 1
FREEMOV_COEF = 0.3


class TreeNode():
    
    def __init__(self, children: list['TreeNode'], grade: float, board: Board, is_base: bool = False) -> None:
        self.children: list['TreeNode'] = children
        self.grade: float = grade
        self.board: Board = board
        self.is_base: bool = is_base

    def setChildren(self, children: list['TreeNode']) -> None:
        self.children = children
    
    def setGrade(self, grade: float) -> None:
        self.grade = grade
        
    def setBoard(self, board: Board) -> None:
        self.board = board
    
    def isBase(self) -> bool:
        return self.is_base

    def isLeaf(self) -> bool:
        return len(self.children) == 0
    
    def print(self) -> None:
        self.visualize()
        
    def visualize(self, level=0):
        indent = " " * (level * 4)
        print(f"{indent}Grade: {self.grade}, Is Base: {self.is_base}")
        for child in self.children:
            if isinstance(child, list):
                for sub_child in child:
                    sub_child.visualize(level + 1)
            else:
                child.visualize(level + 1)

class Fendoter():
    
    def __init__(self, player, grading_method: str, search_depth) -> None:
        self.ref = Referee()
        self.player = player
        self.opponent = 3 - player #TODO: hardcoded, only works for 2 player
        self.grading_method = grading_method
        self.search_depth = search_depth
        self.search_tree: TreeNode = TreeNode([], 0, None, True)
    
    def makeMove(self, board: Board) -> Move:
        best_move: Move = self.evaluateMoves(board, self.grading_method)
        #self.search_tree.print() # debug
        return best_move
    
    def evaluateMoves(self, board: Board, method: str) -> Move:
        match method:
            case "depth1":
                possible_moves, new_boards = self.calculateMoves(board)
                return self.depth1Eval(new_boards, possible_moves)
            case "random":
                possible_moves, new_boards = self.calculateMoves(board)
                return self.randomGrading(possible_moves)
            case "minimax":
                move, grade, self.search_tree = self.minimax(board, depth=self.search_depth, maximizing_player=True)
                return move
            case "negamax":
                move, grade, self.search_tree = self.negamax(board, depth=self.search_depth, p=1)
                return move
            case "alpha-beta":
                move, grade , self.search_tree = self.alphabeta(board, depth=self.search_depth, alpha=float('-inf'), beta=float('inf'), p=1)
                return move
            case _:
                raise ValueError("Invalid grading method")
    
    
    def calculateMoves(self, board: Board) -> tuple[list[Move], list[Board]]:
        # debug start
        #print("\nCurrent Board:\n")
        #print(board)
        # debug end
        
        own_pawns: list[Pawn] = board.getPawns(board.getTurn())
        fields: list[Field] = board.getFieldsFlat()
        board_state: dict = copy.deepcopy(board.getState())

        moves = []
        new_boards = []
        for pawn in own_pawns:
            for field in fields:
                # Place new Pawn
                if self.ref.checkLegalMove(PlacePawn(field.getCoordinates(), board.getTurn()), board_state):
                    moves.append(PlacePawn(field.getCoordinates(), board.getTurn()))
                    new_board = Board(board_state['size'], board_state['max_pawns'])
                    new_board.loadState(copy.deepcopy(board_state))
                    new_board.placePawn(field.getCoordinates(), board.getTurn())
                    new_board.endTurn()
                    new_boards.append(new_board)
                for direction in ["N", "E", "S", "W"]:
                    # Move Pawn and place Wall
                    if self.ref.checkLegalMove(MovePawnAndWall(pawn.getCoordinates(), field.getCoordinates(), direction, board.getTurn()), board_state):
                        moves.append(MovePawnAndWall(pawn.getCoordinates(), field.getCoordinates(), direction, board.getTurn()))
                        new_board = Board(board_state['size'], board_state['max_pawns'])
                        new_board.loadState(copy.deepcopy(board_state))
                        new_board.movePawn(pawn.getCoordinates(), field.getCoordinates())
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        new_boards.append(new_board)
                    # Place Wall without moving Pawn
                    if self.ref.checkLegalMove(PlaceWall(field.getCoordinates(), direction, board.getTurn()), board_state):
                        moves.append(PlaceWall(field.getCoordinates(), direction, board.getTurn()))
                        new_board = Board(board_state['size'], board_state['max_pawns'])
                        new_board.loadState(copy.deepcopy(board_state))
                        new_board.placeWall(field.getCoordinates(), direction, board.getTurn())
                        new_board.endTurn()
                        new_boards.append(new_board)
                        
        return moves, new_boards
    
    
    def randomGrading(self, moves: list[Move]) -> int:
        return random.choice(moves)

    def depth1Eval(self, boards: list[Board], moves: list[Move]) -> Move:
        best_move = boards[0]
        best_grade = self.gradingI(best_move)
        for state in boards:
            grade = self.gradingI(state)
            if grade > best_grade:
                best_move = state
                best_grade = grade
        best_move_index = boards.index(best_move)
        return moves[best_move_index]
    
    def gradingI(self, board: Board) -> int:
        ''' Takes a board and returns the grade for the current player.'''

        current_player = board.getTurn()
        current_opponent = board.getCurrentOpponent()

        board.evaluateFields() # TODO: improve evaluation performance
        if board.getWinner() == board.getTurn():
            return float('inf')

        # grade area
        area_grade = board.getPlayerArea(current_player) - board.getPlayerArea(current_opponent)

        # grade movement freedom
        # freedom_grade = self.calculateMoves(board)[0] # prossessing time too long
        current_pawns = board.getPawns(current_player)
        opponent_pawns = board.getPawns(current_opponent)
        freedom_grade, current_player_freedom_grade, opponent_freedom_grade = 0, 0, 0
        for direction in ["N", "E", "S", "W"]: # estimate freedom by checking walls/pawns/boarders next to pawns
            for pawn in current_pawns:
                end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                if end_coords:
                    if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                        current_player_freedom_grade += 1
            for pawn in opponent_pawns:
                end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                if end_coords:
                    if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                        opponent_freedom_grade += 1

        freedom_grade = (current_player_freedom_grade / len(current_pawns)) - (opponent_freedom_grade / len(opponent_pawns))
        
        grade = AREA_COEF * area_grade + FREEMOV_COEF * freedom_grade
        return grade
        
    def gradingII(self, board: Board) -> int:
        ''' Takes a board and returns the grade for the current player.'''

        current_player = self.player
        current_opponent = self.opponent

        board.evaluateFields() # TODO: improve evaluation performance
        if board.getWinner() == board.getTurn():
            return float('inf')

        # grade area
        area_grade = board.getPlayerArea(current_player) - board.getPlayerArea(current_opponent)

        # grade movement freedom
        # freedom_grade = self.calculateMoves(board)[0] # prossessing time too long
        current_pawns = board.getPawns(current_player)
        opponent_pawns = board.getPawns(current_opponent)
        freedom_grade, current_player_freedom_grade, opponent_freedom_grade = 0, 0, 0
        for direction in ["N", "E", "S", "W"]: # estimate freedom by checking walls/pawns/boarders next to pawns
            for pawn in current_pawns:
                end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                if end_coords:
                    if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                        current_player_freedom_grade += 1
            for pawn in opponent_pawns:
                end_coords = board.getFields()[pawn.getCoordinates()].getNeighborCoords(direction)
                if end_coords:
                    if findValidPath(pawn.getCoordinates(), end_coords, board.getFields()):
                        opponent_freedom_grade += 1

        freedom_grade = (current_player_freedom_grade / len(current_pawns)) - (opponent_freedom_grade / len(opponent_pawns))
        
        grade = AREA_COEF * area_grade + FREEMOV_COEF * freedom_grade
        return grade
        
    def minimax(self, board: Board, depth: int, maximizing_player: bool) -> tuple[int, list[TreeNode]]:
        if depth == 0:
            grade = self.gradingI(board)
            if not maximizing_player:
                grade = -grade
            return None, grade, TreeNode([], grade, board)
        
        children = []
        if maximizing_player:
            max_eval = float('-inf')
            next_moves, new_boards = self.calculateMoves(board)
            for new_board in new_boards:
                _, eval, new_child = self.minimax(new_board, depth - 1, False)
                # debug start
                #print(f"\nNew {self.player} Board (Grade: {eval}):\n")
                #print(new_board)
                # debug end
                children.append(new_child)
                if eval > max_eval:
                    max_eval = eval
                    best_move = next_moves[new_boards.index(new_board)]
            return best_move, max_eval, TreeNode(children, max_eval, board)
        else:
            min_eval = float('inf')
            next_moves, new_boards = self.calculateMoves(board)
            for new_board in new_boards:
                _, eval, new_child = self.minimax(new_board, depth - 1, True)
                # debug start
                #print(f"\nNew {self.opponent} Board (Grade: {eval}):\n")
                #print(new_board)
                # debug end
                children.append(new_child)
                if eval < min_eval:
                    min_eval = eval
                    best_move = next_moves[new_boards.index(new_board)]
            return best_move, min_eval, TreeNode(children, min_eval, board)
        
    
    def negamax(self, board: Board, depth: int, p: int) -> tuple[int, list[TreeNode]]:
        ''' Negamax algorithm 
        p: 1 for player, -1 for opponent
        '''
        if depth == 0:
            grade = p * self.gradingII(board)
            return None, grade, TreeNode([], grade, board)
        
        children = []
        max_eval = -p * float('inf')
        next_moves, new_boards = self.calculateMoves(board)
        for new_board in new_boards:
            _, eval, new_child = self.negamax(new_board, depth - 1, -p)
            # debug start
            #print(f"\nNew {new_board.getTurn()} Board (Grade: {eval}):\n")
            #print(new_board)
            # debug end
            children.append(new_child)
            eval = -eval
            if eval > max_eval:
                max_eval = eval
                best_move = next_moves[new_boards.index(new_board)]
        return best_move, max_eval, TreeNode(children, max_eval, board)
    
    def alphabeta(self, board: Board, depth: int, alpha: int, beta: int, p: int) -> tuple[int, list[TreeNode]]:
        ''' Alpha-Beta Pruning algorithm 
        p: 1 for player, -1 for opponent
        '''
        if depth == 0:
            value = p * self.gradingII(board)
            return None, value, TreeNode([], value, board)
        
        children = []
        value = alpha
        next_moves, new_boards = self.calculateMoves(board)
        for new_board in new_boards:
            _, eval, new_child = self.alphabeta(new_board, depth - 1, -beta, -value, -p)
            children.append(new_child)
            eval = -eval
            if eval > value:
                value = eval
                best_move = next_moves[new_boards.index(new_board)]
                # debug start
                print(f"\nNew {new_board.getTurn()} Board (Grade: {eval}):\n")
                print(new_board)
                # debug end
            if value >= beta:
                return best_move, value, TreeNode(children, value, board)
        return best_move, value, TreeNode(children, value, board)