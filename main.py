import sys
from game import ChessGame
    
def main():
    """
    Main function for running this python script.
    """
    # Default player types
    white_player = "User"
    black_player = "User"
    
    if len(sys.argv) >= 3:

        white_player = sys.argv[1]
        black_player = sys.argv[2]

    game = ChessGame(white_player_type=white_player, black_player_type=black_player)
    game.play(show_ui=True)

if __name__ == '__main__':
    main()
