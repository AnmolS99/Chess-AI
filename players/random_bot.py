from chess_board import ChessBoard
from gui import ChessGUI
from player import Player
import random


class RandomBot():

    def __init__(self, chess_board: ChessBoard, ui: ChessGUI, player: Player) -> None:
        self.chess_board = chess_board
        self.ui = ui
        self.player = player
        
    def make_move(self):
        if self.chess_board.turn == self.player:
            self.chess_board.move_piece(random.choice(self.chess_board.get_all_legal_moves()))