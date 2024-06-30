

import time
from fen_converter import FENConverter
from game import ChessGame


class Tournament:
    """
    Tournament between two bots
    """

    def __init__(self, player1: str, player2: str) -> None:
        self.player1 = player1
        self.player2 = player2

    def play_tournament(self):
        player1_points_sum = 0
        player2_points_sum = 0

        positions_file = open('resources/equal_positions.txt', 'r')
        lines = positions_file.readlines()
        num_games = len(lines)

        fen_converter = FENConverter()

        a = time.time()
        for line in lines:
                game = ChessGame(white_player_type=self.player1, black_player_type=self.player2)
                fen_converter.to_game_state(game.chess_board, line.strip("\n"))
                
                player1_points, player2_points = game.play(show_ui=False)
                player1_points_sum += player1_points
                player2_points_sum += player2_points
        b = time.time()
        print(f"{self.player1}: {player1_points_sum} - {self.player2}: {player2_points_sum}\nTournament of {num_games} games took {b - a} sec (avg time {(b-a)/num_games})")

t = Tournament("AlphaBeta", "AlphaBetaV2")
t.play_tournament()
