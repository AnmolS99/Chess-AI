from chess_board import ChessBoard
from gui import ChessGUI
from player import Player
import numpy as np


class AlphaBetaBot():

    def __init__(self, chess_board: ChessBoard, ui: ChessGUI, player: Player) -> None:
        self.chess_board = chess_board
        self.ui = ui
        self.player = player
        
    def make_move(self):
        if self.chess_board.turn == self.player:
            self.chess_board.move_piece(self.minimax())

    def minimax(self, depth: int = 3):
        """
        Return action that gives that max-value (if player is white) or min-value (if player is black) in the current state
        """
        alpha = -np.inf
        beta = np.inf
        if self.player == Player.white:
            max_value_move = None
            max_value = -np.inf
            for move in self.chess_board.get_all_legal_moves():
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = self.min_value(chess_board_copy, depth - 1, alpha, beta)
                if min_value > max_value:
                    max_value = min_value
                    max_value_move = move
                alpha = max(alpha, max_value)
            return max_value_move
        else:
            min_value_move = None
            min_value = np.inf
            for move in self.chess_board.get_all_legal_moves():
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                max_value = self.max_value(chess_board_copy, depth - 1, alpha, beta)
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
                return 1000
            elif black_points == 1:
                return -1000
            else:
                return 0
        elif depth == 0:
            return chess_board.get_points()[Player.white]
        else:
            max_value = -np.inf
            for move in chess_board.get_all_legal_moves():
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
                return 1000
            elif black_points == 1:
                return -1000
            else:
                return 0
        elif depth == 0:
            return chess_board.get_points()[Player.white]
        else:
            min_value = np.inf
            for move in chess_board.get_all_legal_moves():
                chess_board_copy = chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = min(min_value, self.max_value(chess_board_copy, depth - 1, alpha, beta))
                if min_value <= alpha:
                    return min_value
                beta = min(beta, min_value)
            return min_value