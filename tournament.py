

import time
from game import ChessGame


class Tournament:
    """
    Tournament between two players
    """

    def __init__(self, player1: str, player2: str) -> None:
        self.player1 = player1
        self.player2 = player2

    def play_tournament(self, num_games: int):
        player1_points_sum = 0
        player2_points_sum = 0
        a = time.time()
        for i in range(num_games):
            if i % 2 == 0:
                game = ChessGame(white_player_type=self.player1, black_player_type=self.player2)
                player1_points, player2_points = game.play(show_ui=False)
            else:
                game = ChessGame(white_player_type=self.player2, black_player_type=self.player1)
                player2_points, player1_points = game.play(show_ui=False)
            player1_points_sum += player1_points
            player2_points_sum += player2_points
        b = time.time()
        print(f"{self.player1}: {player1_points_sum} - {self.player2}: {player2_points_sum}\nTournament of {num_games} games took {b - a} sec (avg time {(b-a)/num_games})")

t = Tournament("AlphaBeta", "AlphaBetaV2")
t.play_tournament(10)
