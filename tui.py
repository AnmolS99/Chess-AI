class ChessTUI:

    icon_dict = {1: "♙", 2: "♖", 3: "♘", 4: "♗", 5: "♕", 6: "♔", -1: "♟", -2: "♜", -3: "♞", -4: "♝", -5: "♛", -6: "♚"}
    
    def print_game(self, game):
        """Prints the game board to the console."""
        print("\n")
        print("    A  B  C  D  E  F  G  H")
        print("   ------------------------", end="")
        for i in range(8):
            print("\n" + str(8 - i) + " |", end="")
            for j in range(8):
                if game.board[i][j] == 0:
                    print(" - ", end="")
                else:
                    print(" " + self.icon_dict[game.board[i][j]] + " ", end="")
            print("| " + str(8 - i))
        print("   ------------------------")
        print("    A  B  C  D  E  F  G  H")
        print("\n")
