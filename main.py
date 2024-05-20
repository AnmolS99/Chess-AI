import time
from chess_board import ChessBoard
from fen_converter import FENConverter
from gui import ChessGUI
    
def main():
    """
    Main function for running this python script.
    """
    fen_converter = FENConverter()
    game = ChessBoard()
    game.reset_board()
    fen_converter.to_game_state(game, "7k/8/8/5Q2/8/8/8/K7 w - - 0 1")
    
    ui = ChessGUI(game)
    
    ui.print_game()
    ui.root.update()  # Update the GUI
    ui.root.mainloop()

if __name__ == '__main__':
    main()
