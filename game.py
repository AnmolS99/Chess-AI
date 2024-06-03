from players.random_bot import RandomBot
from players.user import User
from chess_board import ChessBoard
from gui import ChessGUI
from player import Player, PlayerType
import random
import time


class ChessGame():

    def __init__(self, white_player_type: PlayerType = PlayerType.User.name, black_player_type: PlayerType = PlayerType.User.name) -> None:
        self.chess_board = ChessBoard()
        self.chess_board.reset_board()
        self.ui = ChessGUI(self.chess_board)
        self.white_player_type = white_player_type
        self.black_player_type = black_player_type

    def play(self):

        white_player = self.get_player(self.white_player_type, Player.white)
        black_player = self.get_player(self.black_player_type, Player.black)
        self.ui.print_game()
        self.ui.root.update()

        finished = False

        while True:
            if self.chess_board.turn == Player.white and not finished:
                white_player.make_move()
                self.ui.print_game()
                self.ui.root.update()
            else:
                black_player.make_move()
                self.ui.print_game()
                self.ui.root.update()
            

            finished, white_points, black_points = self.chess_board.is_finished()
            if finished:
                self.ui.print_game()
                self.ui.root.update()
                self.ui.root.wait_variable(self.ui.clicked)
                self.ui.clicked.set(False)
                self.ui.root.update()

    def get_player(self, player_type, player):
        if player_type == PlayerType.Random.name:
            return RandomBot(self.chess_board, self.ui, player)
        elif player_type == PlayerType.User.name:
            return User(self.chess_board, self.ui, player)
        else:
            Exception(f"Invalid player_type: {player_type}")