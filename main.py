from game import ChessGame
    
def main():
    """
    Main function for running this python script.
    """
    game = ChessGame(white_player_type="Random", black_player_type="MiniMax")
    game.play()

if __name__ == '__main__':
    main()
