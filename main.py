import time
from chess_board import ChessBoard
from fen_converter import FENConverter
from gui import ChessGUI
import os

@staticmethod
def move_sim(game: ChessBoard, ui, curr_depth: int, final_depth: int):

    if curr_depth == final_depth:
        return 1
    else:
        org_game = game.copy()
        num_positions = 0
        for move in org_game.get_all_legal_moves():
            # print(f"Evaluating {move}")
            game_with_move = org_game.copy()
            game_with_move.move_piece(move)
            # ui.game = game_with_move
            # ui.print_game()
            # ui.root.update()  # Update the GUI
            # time.sleep(0.01)  # Pause for one second
            # print(move)
            num_positions_given_move = move_sim(game_with_move, ui, curr_depth + 1, final_depth)
            num_positions += num_positions_given_move
            if curr_depth == 0:
                print(f"{move}: {num_positions_given_move}")
                with open('./output/my_program_output.txt', 'a') as f:
                    f.write(f"{move}: {num_positions_given_move}\n")
        return num_positions
    
def main():
    """
    Main function for running this python script.
    """
    fen_converter = FENConverter()
    game = ChessBoard()
    game.reset_board()
    fen_converter.to_game_state(game, "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
    
    ui = ChessGUI(game)
    
    with open('./output/my_program_output.txt', 'w'):
        pass
    
    # ui.print_game()
    # ui.root.update()  # Update the GUI
    # ui.root.mainloop()
    
    for i in range(1, 4):   # TODO: Number of nodes for Postiton 5 fails here
        start = time.time()
        num_nodes = move_sim(game, ui, 0, i)
        end = time.time()
        print(f"Depth {i}: {num_nodes} nodes ({end-start}) seconds")

    # start = time.time()
    # depth = 4
    # num_nodes = move_sim(game, ui, 0, depth)
    # end = time.time()
    # print(f"Depth {depth}: {num_nodes} nodes ({end-start}) seconds")

if __name__ == '__main__':
    main()


