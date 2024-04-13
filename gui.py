from PIL import Image, ImageTk, ImageDraw
from tkinter import Canvas, PhotoImage, Tk
from chess_board import ChessBoard

from player import Player


class ChessGUI:


    def __init__(self, game: ChessBoard, board_size=640, info_size=50):
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
        self.shade_image = self.get_shade_image()

    def print_game(self):
        self.canvas.delete("all")
        # Display board
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = "white"
                else:
                    color = "#5f6087"
                self.canvas.create_rectangle(
                    col * self.square_size, (row * self.square_size) + self.info_size, (col + 1) * self.square_size, ((row + 1) * self.square_size) + self.info_size, fill=color
                )
                piece = self.game.board[row][col]
                if piece != 0:

                    self.canvas.create_image(
                        col * self.square_size + self.square_size // 2, (row * self.square_size + self.square_size // 2) + self.info_size, image = self.icon_dict[piece]
                    )

        # Display selected piece legal moves
        if self.selected_pos is not None:
            for move in self.game.get_legal_moves(self.selected_pos):
                row, col = move
                self.canvas.create_rectangle(
                    col * self.square_size, (row * self.square_size) + self.info_size, (col + 1) * self.square_size, ((row + 1) * self.square_size) + self.info_size, outline="red", width=3
                )

        # Display player info
        player_color = self.game.turn.name
        self.canvas.create_text(60, self.info_size // 2, text=f"Player: Black", font=("Arial", 18))
        self.canvas.create_text(60, self.board_size + self.info_size + self.info_size // 2, text=f"Player: White", font=("Arial", 18))

        # Button to reset the game
        self.canvas.create_rectangle(self.board_size - 100, self.info_size // 2 - 20, self.board_size, self.info_size // 2 + 20, fill="green")
        self.canvas.create_text(self.board_size - 50, self.info_size // 2, text="Reset", font=("Arial", 18))



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

        # Display check info
        if self.game.is_in_check(self.game.board, Player.black):
            self.canvas.create_text(300, self.info_size // 2, text="Black player in check!", font=("Arial", 18))
        if self.game.is_in_check(self.game.board, Player.white):
            self.canvas.create_text(300, self.board_size + self.info_size + self.info_size // 2, text="White player in check!", font=("Arial", 18))



        # Display checkmate info
        if self.game.is_checkmate():
            winner_player = "white" if self.game.turn == Player.black else "black"
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text( self.board_size // 2, (self.board_size + self.info_size) // 2, text=f"Checkmate! {winner_player} wins!", font=("Arial", 26))
            self.canvas.create_text( self.board_size // 2, ((self.board_size + self.info_size) // 2) + 50, text=f"Click on reset button in top left corner to begin a new game", font=("Arial", 18))
            

        self.root.mainloop()
        

    def on_click(self, event):
        # If below the board, do nothing
        if event.y > self.board_size + self.info_size:
            return
        # If clicked on the reset button
        elif self.board_size - 100 < event.x < self.board_size and self.info_size // 2 - 20 < event.y < self.info_size // 2 + 20:
            print("Game reset")
            self.selected_pos = None
            self.game.reset_board()
            self.print_game()
            return
        col = event.x // self.square_size
        row = (event.y - self.info_size) // self.square_size # Account for the space above the board
        print(f"Clicked on {row}, {col}")
        if self.selected_pos is not None:
            if (row, col) in self.game.get_legal_moves(self.selected_pos):
                self.game.move_piece(self.selected_pos, (row, col))
            self.selected_pos = None
        elif self.game.board[row][col] * self.game.turn.value > 0:
            self.selected_pos = (row, col)
        else:
            self.selected_pos = None
            return
        self.print_game()

    def get_shade_image(self):
        # Create a new image with the same size as the canvas
        image = Image.new('RGBA', (self.board_size, self.board_size + self.info_size*2))

        # Draw a semi-transparent black rectangle on the image
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), image.size], fill=(0, 0, 0, 128))  # RGBA color

        # Convert the PIL image to a PhotoImage
        photo = ImageTk.PhotoImage(image)
        return photo