from tkinter import Canvas, PhotoImage, Tk


class ChessGUI:


    def __init__(self, game, window_size=720):
        self.game = game
        self.selected_pos = None
        self.root = Tk()
        self.canvas = Canvas(self.root, width=window_size, height=window_size)
        self.square_size = window_size // 8
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.icon_dict = {1: PhotoImage(file="./assets/white_pawn.png"), 2: PhotoImage(file="./assets/white_rook.png"), 3: PhotoImage(file="./assets/white_knight.png"), 4: PhotoImage(file="./assets/white_bishop.png"), 5: PhotoImage(file="./assets/white_queen.png"), 6: PhotoImage(file="./assets/white_king.png"), -1: PhotoImage(file="./assets/black_pawn.png"), -2: PhotoImage(file="./assets/black_rook.png"), -3: PhotoImage(file="./assets/black_knight.png"), -4: PhotoImage(file="./assets/black_bishop.png"), -5: PhotoImage(file="./assets/black_queen.png"), -6: PhotoImage(file="./assets/black_king.png")}

    def print_game(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = "white"
                else:
                    color = "grey"
                self.canvas.create_rectangle(
                    col * self.square_size, row * self.square_size, (col + 1) * self.square_size, (row + 1) * self.square_size, fill=color
                )
                piece = self.game.board[row][col]
                if piece != 0:

                    self.canvas.create_image(
                        col * self.square_size + 50, row * self.square_size + 50, image = self.icon_dict[piece]
                    )
        if self.selected_pos is not None:
            for move in self.game.get_possible_moves(self.selected_pos):
                row, col = move
                self.canvas.create_rectangle(
                    col * self.square_size, row * self.square_size, (col + 1) * self.square_size, (row + 1) * self.square_size, outline="red"
                )
        self.root.mainloop()
        

    def on_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size
        print(f"Clicked on {row}, {col}")
        if self.selected_pos is not None:
            if (row, col) in self.game.get_possible_moves(self.selected_pos):
                self.game.move_piece(self.selected_pos, (row, col))
                self.selected_pos = None
        self.selected_pos = (row, col)
        self.print_game()