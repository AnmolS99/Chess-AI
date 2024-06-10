from game import ChessGame
    
def main():
    """
    Main function for running this python script.
    """
    game = ChessGame(white_player_type="User", black_player_type="AlphaBeta")
    game.play(show_ui=True)

if __name__ == '__main__':
    main()
