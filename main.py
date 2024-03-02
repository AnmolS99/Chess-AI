from chess_board import ChessBoard
from gui import ChessGUI
import tui

def main():
    """
    Main function for running this python script.
    """
    game = ChessBoard()
    game.reset_board()
    ui = ChessGUI(game)
    ui.print_game()

if __name__ == '__main__':
    main()


