from tkinter import Canvas, PhotoImage, Tk

from player import Player


class ChessGUI:


    def __init__(self, game, board_size=640, info_size=50):
        self.game = game
        self.board_size = board_size
        self.info_size = info_size
        self.selected_pos = None
        self.root = Tk()
        self.canvas = Canvas(self.root, width=board_size, height=board_size + info_size*2)
        self.square_size = board_size // 8
        self.canvas.pack()
        self.subsampled_images = []
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
                    col * self.square_size, (row * self.square_size) + self.info_size, (col + 1) * self.square_size, ((row + 1) * self.square_size) + self.info_size, fill=color
                )
                piece = self.game.board[row][col]
                if piece != 0:

                    self.canvas.create_image(
                        col * self.square_size + self.square_size // 2, (row * self.square_size + self.square_size // 2) + self.info_size, image = self.icon_dict[piece]
                    )
        if self.selected_pos is not None:
            for move in self.game.get_possible_moves(self.selected_pos):
                row, col = move
                self.canvas.create_rectangle(
                    col * self.square_size, (row * self.square_size) + self.info_size, (col + 1) * self.square_size, ((row + 1) * self.square_size) + self.info_size, outline="red"
                )
        # Display player info
        player_color = self.game.turn.name
        self.canvas.create_text(60, self.info_size // 2, text=f"Player: Black", font=("Arial", 18))
        self.canvas.create_text(60, self.board_size + self.info_size + self.info_size // 2, text=f"Player: White", font=("Arial", 18))

        # Display captured pieces as small icons
        self.subsampled_images.clear()
        for i, piece in enumerate(self.game.captured_pieces[Player.black]):
            image = self.icon_dict[piece].subsample(2, 2)  # Reduce the size of the image by a factor of 2
            self.subsampled_images.append(image)
            self.canvas.create_image(160 + i * 40, self.info_size // 2, image=image)

        for i, piece in enumerate(self.game.captured_pieces[Player.white]):
            image = self.icon_dict[piece].subsample(2, 2)  # Reduce the size of the image by a factor of 2
            self.subsampled_images.append(image)
            self.canvas.create_image(160 + i * 40, self.board_size + self.info_size + self.info_size // 2, image=image)

        self.root.mainloop()
        

    def on_click(self, event):
        # If below the board, do nothing
        if event.y > self.board_size + self.info_size:
            return
        col = event.x // self.square_size
        row = (event.y - self.info_size) // self.square_size # Account for the space above the board
        print(f"Clicked on {row}, {col}")
        if self.selected_pos is not None:
            if (row, col) in self.game.get_possible_moves(self.selected_pos):
                self.game.move_piece(self.selected_pos, (row, col))
            self.selected_pos = None
        else:
            self.selected_pos = (row, col)
        self.print_game()