import time
from chess_board import ChessBoard
from fen_converter import FENConverter
from gui import ChessGUI
from player import Player
import random
    
def main():
    """
    Main function for running this python script.
    """
    game = ChessBoard()
    game.reset_board()
    
    ui = ChessGUI(game)
    
    ui.print_game()
    ui.root.update()
    # ui.root.mainloop()

    while True:
        game.move_piece(random.choice(game.get_all_legal_moves()))
        ui.print_game()
        ui.root.update()
        # time.sleep(0.01)

        finished, white_points, black_points = game.is_finished()
        if finished:
            ui.print_game()
            ui.root.update()
            time.sleep(5)
            print(f"White points: {white_points}, black points: {black_points}")
            break

if __name__ == '__main__':
    main()
