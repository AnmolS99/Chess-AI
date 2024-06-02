from chess_board import ChessBoard
from gui import ChessGUI
from player import Player
import random


class User():

    def __init__(self, chess_board: ChessBoard, ui: ChessGUI, player: Player) -> None:
        self.chess_board = chess_board
        self.ui = ui
        self.player = player
        
    def make_move(self):
        self.ui.root.wait_variable(self.ui.clicked)
        self.ui.clicked.set(False)
        self.ui.root.update()