from chess_board import ChessBoard
from gui import ChessGUI
from player import Player
import numpy as np

square_eval = { 
# Pawn
1: [
 [0,  0,  0,  0,  0,  0,  0,  0],
[50, 50, 50, 50, 50, 50, 50, 50],
[10, 10, 20, 30, 30, 20, 10, 10],
 [5,  5, 10, 25, 25, 10,  5,  5],
 [0,  0,  0, 20, 20,  0,  0,  0],
 [5, -5,-10,  0,  0,-10, -5,  5],
 [5, 10, 10,-20,-20, 10, 10,  5],
 [0,  0,  0,  0,  0,  0,  0,  0]
 ],

# Rook
 2: [
 [0,  0,  0,  0,  0,  0,  0,  0],
  [5, 10, 10, 10, 10, 10, 10,  5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
  [0,  0,  0,  5,  5,  0,  0,  0]
  ],

  # Knight
  3: [
[ -50,-40,-30,-30,-30,-30,-40,-50],
[-40,-20,  0,  0,  0,  0,-20,-40],
[-30,  0, 10, 15, 15, 10,  0,-30],
[-30,  5, 15, 20, 20, 15,  5,-30],
[-30,  0, 15, 20, 20, 15,  0,-30],
[-30,  5, 10, 15, 15, 10,  5,-30],
[-40,-20,  0,  5,  5,  0,-20,-40],
[-50,-40,-30,-30,-30,-30,-40,-50],
  ],

  # Bishop
  4: [
[-20,-10,-10,-10,-10,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5, 10, 10,  5,  0,-10],
[-10,  5,  5, 10, 10,  5,  5,-10],
[-10,  0, 10, 10, 10, 10,  0,-10],
[-10, 10, 10, 10, 10, 10, 10,-10],
[-10,  5,  0,  0,  0,  0,  5,-10],
[-20,-10,-10,-10,-10,-10,-10,-20],
  ],

# Queen
  5: [
[-20,-10,-10, -5, -5,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5,  5,  5,  5,  0,-10],
 [-5,  0,  5,  5,  5,  5,  0, -5],
  [0,  0,  5,  5,  5,  5,  0, -5],
[-10,  5,  5,  5,  5,  5,  0,-10],
[-10,  0,  5,  0,  0,  0,  0,-10],
[-20,-10,-10, -5, -5,-10,-10,-20]
  ],

# King (middlegame)
  6: [
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-20,-30,-30,-40,-40,-30,-30,-20],
[-10,-20,-20,-20,-20,-20,-20,-10],
[ 20, 20,  0,  0,  0,  0, 20, 20],
[ 20, 30, 10,  0,  0, 10, 30, 20]
  ]}

class AlphaBetaBotV2():

    def __init__(self, chess_board: ChessBoard, ui: ChessGUI, player: Player, depth: int = 3, move_ordering = True) -> None:
        self.chess_board = chess_board
        self.ui = ui
        self.player = player
        self.depth = depth
        self.move_ordering = move_ordering
        
    def make_move(self):
        if self.chess_board.turn == self.player:
            self.chess_board.move_piece(self.minimax())

    def minimax(self):
        """
        Return action that gives that max-value (if player is white) or min-value (if player is black) in the current state
        """
        alpha = -np.inf
        beta = np.inf
        if self.player == Player.white:
            max_value_move = None
            max_value = -np.inf
            for move in self.chess_board.get_all_legal_moves(move_ordering=self.move_ordering):
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = self.min_value(chess_board_copy, self.depth - 1, alpha, beta)
                if min_value > max_value:
                    max_value = min_value
                    max_value_move = move
                alpha = max(alpha, max_value)
            return max_value_move
        else:
            min_value_move = None
            min_value = np.inf
            for move in self.chess_board.get_all_legal_moves(move_ordering=self.move_ordering):
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                max_value = self.max_value(chess_board_copy, self.depth - 1, alpha, beta)
                if max_value < min_value:
                    min_value = max_value
                    min_value_move = move
                beta = min(beta, min_value)
            return min_value_move

    def max_value(self, chess_board: ChessBoard, depth: int, alpha, beta):
        """
        Returns max-value points (captures) for white player
        """
        is_finished, white_points, black_points = chess_board.is_finished()
        if is_finished:
            if white_points == 1:
                return np.inf
            elif black_points == 1:
                return -np.inf
            else:
                return 0
        elif depth == 0:
            return self.eval_state(chess_board)
        else:
            max_value = -np.inf
            for move in chess_board.get_all_legal_moves(move_ordering=self.move_ordering):
                chess_board_copy = chess_board.copy()
                chess_board_copy.move_piece(move)
                max_value = max(max_value, self.min_value(chess_board_copy, depth - 1, alpha, beta))
                if max_value >= beta:
                    return max_value
                alpha = max(alpha, max_value)
            return max_value

    def min_value(self, chess_board: ChessBoard, depth: int, alpha, beta):
        """
        Returns min-value points (captures) for white player
        """
        is_finished, white_points, black_points = chess_board.is_finished()
        if is_finished:
            if white_points == 1:
                return np.inf
            elif black_points == 1:
                return -np.inf
            else:
                return 0
        elif depth == 0:
            return self.eval_state(chess_board)
        else:
            min_value = np.inf
            for move in chess_board.get_all_legal_moves(move_ordering=self.move_ordering):
                chess_board_copy = chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = min(min_value, self.max_value(chess_board_copy, depth - 1, alpha, beta))
                if min_value <= alpha:
                    return min_value
                beta = min(beta, min_value)
            return min_value
    
    def eval_state(self, chess_board: ChessBoard):
        evaluation = chess_board.get_points()[Player.white] * 1000
        for row in range(8):
            for col in range(8):
                piece = chess_board.board[row][col]
                if piece == 0:
                    continue
                elif piece > 0:
                    evaluation += square_eval[piece][row][col]
                elif piece < 0:
                    evaluation -= square_eval[abs(piece)][7 - row][col]
        return evaluation