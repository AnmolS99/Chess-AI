

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
        a = time.time()
        for i in range(num_games):
            if i % 2 == 0:
                game = ChessGame(white_player_type=self.player1, black_player_type=self.player2)
                game.play(show_ui=False)
            else:
                game = ChessGame(white_player_type=self.player2, black_player_type=self.player1)
                game.play(show_ui=False)
            print(f"Game {i + 1} finished")
        b = time.time()
        print(f"Tournament of {num_games} games took {b - a} sec (avg time {(b-a)/num_games})")

t = Tournament("Random", "AlphaBeta")
t.play_tournament(10)
