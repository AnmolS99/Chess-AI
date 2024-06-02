import time
from chess_board import ChessBoard
from fen_converter import FENConverter
from game import ChessGame
from gui import ChessGUI
from player import Player
import random
    
def main():
    """
    Main function for running this python script.
    """
    game = ChessGame(white_player_type="Random", black_player_type="User")
    game.play()

if __name__ == '__main__':
    main()
