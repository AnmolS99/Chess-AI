from chess_board import ChessBoard
from gui import ChessGUI
from player import Player
import random


class MiniMaxBot():

    def __init__(self, chess_board: ChessBoard, ui: ChessGUI, player: Player) -> None:
        self.chess_board = chess_board
        self.ui = ui
        self.player = player
        
    def make_move(self):
        if self.chess_board.turn == self.player:
            self.chess_board.move_piece(self.minimax())

    def minimax(self, depth: int = 2):
        """
        Return action that gives that max-value (if player is white) or min-value (if player is black) in the current state
        """
        if self.player == Player.white:
            max_value_move = None
            max_value = None
            for move in self.chess_board.get_all_legal_moves():
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = self.min_value(chess_board_copy, depth - 1)
                if max_value == None or min_value > max_value:
                    max_value = min_value
                    max_value_move = move
            return max_value_move
        else:
            min_value_move = None
            min_value = None
            for move in self.chess_board.get_all_legal_moves():
                chess_board_copy = self.chess_board.copy()
                chess_board_copy.move_piece(move)
                max_value = self.max_value(chess_board_copy, depth - 1)
                if min_value == None or max_value < min_value:
                    min_value = max_value
                    min_value_move = move
            return min_value_move

    def max_value(self, chess_board: ChessBoard, depth: int):
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
            max_value = None
            for move in chess_board.get_all_legal_moves():
                chess_board_copy = chess_board.copy()
                chess_board_copy.move_piece(move)
                min_value = self.min_value(chess_board_copy, depth - 1)
                if max_value == None or min_value > max_value:
                    max_value = min_value
            return max_value

    def min_value(self, chess_board: ChessBoard, depth: int):
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
            min_value = None
            for move in chess_board.get_all_legal_moves():
                chess_board_copy = chess_board.copy()
                chess_board_copy.move_piece(move)
                max_value = self.max_value(chess_board_copy, depth - 1)
                if min_value == None or max_value < min_value:
                    min_value = max_value
            return min_value