from players.alpha_beta_bot import AlphaBetaBot
from players.alpha_beta_bot_v2 import AlphaBetaBotV2
from players.minimax_bot import MiniMaxBot
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
        self.ui = ChessGUI(self.chess_board, white_player_type, black_player_type)
        self.white_player_type = white_player_type
        self.black_player_type = black_player_type

    def play(self, show_ui=True):

        white_player = self.get_player(self.white_player_type, Player.white)
        black_player = self.get_player(self.black_player_type, Player.black)
        if show_ui:
            self.ui.print_game()
            self.ui.root.update()

        finished = False
        while not finished:
            if self.chess_board.turn == Player.white and not finished:
                white_player.make_move()
                if self.ui.win_closed:
                    return
                if show_ui:
                    self.ui.print_game()
                    self.ui.root.update()
            else:
                black_player.make_move()
                if self.ui.win_closed:
                    return
                if show_ui:
                    self.ui.print_game()
                    self.ui.root.update()
            

            finished, white_points, black_points = self.chess_board.is_finished()
            if finished:
                if show_ui:
                    self.ui.print_game()
                    self.ui.root.update()
                    self.ui.root.wait_variable(self.ui.clicked)
                    self.ui.clicked.set(False)
                    self.ui.root.update()
                else:
                    print(f"White player points: {white_points} - Black player points: {black_points}")
        return white_points, black_points

    def get_player(self, player_type, player):
        if player_type == PlayerType.User.name:
            return User(self.chess_board, self.ui, player)
        elif player_type == PlayerType.Random.name:
            return RandomBot(self.chess_board, self.ui, player)
        elif player_type == PlayerType.MiniMax.name:
            return MiniMaxBot(self.chess_board, self.ui, player)
        elif player_type == PlayerType.AlphaBeta.name:
            return AlphaBetaBot(self.chess_board, self.ui, player)
        elif player_type == PlayerType.AlphaBetaV2.name:
            return AlphaBetaBotV2(self.chess_board, self.ui, player)
        else:
            raise Exception(f"Invalid player_type: {player_type}. Valid player types: {[ptype.name for ptype in PlayerType]}")