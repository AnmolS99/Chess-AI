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
    fen_converter.to_game_state(game, "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
    
    ui = ChessGUI(game)
    
    ui.print_game()
    ui.root.update()  # Update the GUI
    ui.root.mainloop()

if __name__ == '__main__':
    main()
