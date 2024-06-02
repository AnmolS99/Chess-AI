from PIL import Image, ImageTk, ImageDraw
from tkinter import Canvas, PhotoImage, Tk, BooleanVar
from chess_board import ChessBoard
from player import Player


class ChessGUI:


    def __init__(self, game: ChessBoard, board_size=640, player_info_size=50, game_info_size=20):
        self.game = game
        self.board_size = board_size
        self.player_info_size = player_info_size
        self.game_info_size = game_info_size
        self.info_size = self.player_info_size + self.game_info_size 
        self.show_promotion = False
        self.promotion_piece = None
        self.promotion_to_square = None
        self.selected_pos = None
        self.root = Tk()
        self.canvas = Canvas(self.root, width=board_size, height=board_size + player_info_size*2 + game_info_size)
        self.square_size = board_size // 8
        self.canvas.pack()
        self.subsampled_images = []
        self.canvas.bind("<Button-1>", self.on_click)
        self.icon_dict = {1: PhotoImage(file="./assets/white_pawn.png"), 2: PhotoImage(file="./assets/white_rook.png"), 3: PhotoImage(file="./assets/white_knight.png"), 4: PhotoImage(file="./assets/white_bishop.png"), 5: PhotoImage(file="./assets/white_queen.png"), 6: PhotoImage(file="./assets/white_king.png"), -1: PhotoImage(file="./assets/black_pawn.png"), -2: PhotoImage(file="./assets/black_rook.png"), -3: PhotoImage(file="./assets/black_knight.png"), -4: PhotoImage(file="./assets/black_bishop.png"), -5: PhotoImage(file="./assets/black_queen.png"), -6: PhotoImage(file="./assets/black_king.png")}
        self.shade_image = self.get_shade_image()
        self.clicked = BooleanVar(value=False)

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
                piece = int(self.game.board[row][col])
                if piece != 0:

                    self.canvas.create_image(
                        col * self.square_size + self.square_size // 2, (row * self.square_size + self.square_size // 2) + self.info_size, image = self.icon_dict[piece]
                    )

        # Display selected piece legal moves
        if self.selected_pos is not None:
            for (_, end_pos, _) in self.game.get_legal_moves(self.selected_pos):
                row, col = end_pos
                self.canvas.create_rectangle(
                    col * self.square_size, (row * self.square_size) + self.info_size, (col + 1) * self.square_size, ((row + 1) * self.square_size) + self.info_size, outline="red", width=3
                )

        # Display move number
        self.canvas.create_text(60, self.game_info_size, text=f"Move #{self.game.num_moves}", font=("Arial", 18), fill= "Gray")

        # Display player info
        player_turn = self.game.turn
        player_points = self.game.get_points()
        self.canvas.create_text(60, (self.player_info_size // 2) + self.game_info_size, text=f"Black ({player_points[Player.black]})", font=("Arial", 18), fill= "green" if player_turn == Player.black else "white")
        self.canvas.create_text(60, self.board_size + self.info_size + self.player_info_size // 2, text=f"White ({player_points[Player.white]})", font=("Arial", 18), fill= "green" if player_turn == Player.white else "white")

        # Button to reset the game
        self.canvas.create_rectangle(self.board_size - 100, (self.player_info_size // 2) + self.game_info_size - 20, self.board_size, (self.player_info_size // 2) + self.game_info_size + 20, fill="green")
        self.canvas.create_text(self.board_size - 50, (self.player_info_size // 2) + self.game_info_size, text="Reset", font=("Arial", 18))

        # Display captured pieces as small icons
        self.subsampled_images.clear()
        for i, piece in enumerate(self.game.captured_pieces[Player.black]):
            image = self.icon_dict[piece].subsample(2, 2)  # Reduce the size of the image by a factor of 2
            self.subsampled_images.append(image)
            self.canvas.create_image(160 + i * 40, (self.player_info_size // 2) + self.game_info_size, image=image)

        for i, piece in enumerate(self.game.captured_pieces[Player.white]):
            image = self.icon_dict[piece].subsample(2, 2)  # Reduce the size of the image by a factor of 2
            self.subsampled_images.append(image)
            self.canvas.create_image(160 + i * 40, self.board_size + self.info_size + self.player_info_size // 2, image=image)
        
        # Display checkmate info
        if self.game.is_checkmate():
            winner_player = "White" if self.game.turn == Player.black else "Black"
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text(self.board_size // 2, (self.board_size + self.info_size) // 2, text=f"Checkmate! {winner_player} wins!", font=("Arial", 26))
            self.canvas.create_text(self.board_size // 2, ((self.board_size + self.info_size) // 2) + 50, text="Click on reset button in top right corner to begin a new game", font=("Arial", 18))
        
        # Display stalemate info
        elif self.game.is_stalemate():
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text(self.board_size // 2, (self.board_size + self.info_size) // 2, text="Stalemate! Draw!", font=("Arial", 26))
            self.canvas.create_text(self.board_size // 2, ((self.board_size + self.info_size) // 2) + 50, text="Click on reset button in top right corner to begin a new game", font=("Arial", 18))
        
        # Display dead position info
        elif self.game.is_dead_position():
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text(self.board_size // 2, (self.board_size + self.info_size) // 2, text="Dead position! Draw!", font=("Arial", 26))
            self.canvas.create_text(self.board_size // 2, ((self.board_size + self.info_size) // 2) + 50, text="Click on reset button in top right corner to begin a new game", font=("Arial", 18))
        
        elif self.game.has_reached_move_limit():
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text(self.board_size // 2, (self.board_size + self.info_size) // 2, text="Move Limit Reached! Draw!", font=("Arial", 26))
            self.canvas.create_text(self.board_size // 2, ((self.board_size + self.info_size) // 2) + 50, text="Click on reset button in top right corner to begin a new game", font=("Arial", 18))
        
        # Display check info
        elif self.game.is_in_check(self.game.board, Player.black):
            self.canvas.create_text(300, self.game_info_size // 2, text="Black player in check!", font=("Arial", 18))
        elif self.game.is_in_check(self.game.board, Player.white):
            self.canvas.create_text(300, self.game_info_size, text="White player in check!", font=("Arial", 18))
        
        # Display promotion options
        if self.show_promotion:
            self.canvas.create_image(0, 0, image=self.shade_image, anchor='nw')
            self.canvas.create_text( self.board_size // 2, ((self.board_size + self.info_size) // 2) - 50, text="Choose a piece to promote to", font=("Arial", 26))
            self.canvas.create_image(150, ((self.board_size + self.info_size) // 2) + 50, image=self.icon_dict[2*self.game.turn.value])
            self.canvas.create_image(250, ((self.board_size + self.info_size) // 2) + 50, image=self.icon_dict[3*self.game.turn.value])
            self.canvas.create_image(350, ((self.board_size + self.info_size) // 2) + 50, image=self.icon_dict[4*self.game.turn.value])
            self.canvas.create_image(450, ((self.board_size + self.info_size) // 2) + 50, image=self.icon_dict[5*self.game.turn.value])
        

    def on_click(self, event):
        if self.show_promotion and self.promotion_piece is None:
            y_range_start = ((self.board_size + self.info_size) // 2)
            y_range_end = ((self.board_size + self.info_size) // 2) + 100
            if 100 < event.x <= 200 and y_range_start < event.y < y_range_end:
                self.game.move_piece((self.selected_pos, self.promotion_to_square, 2*self.game.turn.value))
            elif 200 < event.x <= 300 and y_range_start < event.y < y_range_end:
                self.game.move_piece((self.selected_pos, self.promotion_to_square, 3*self.game.turn.value))
            elif 300 < event.x <= 400 and y_range_start < event.y < y_range_end:
                self.game.move_piece((self.selected_pos, self.promotion_to_square, 4*self.game.turn.value))
            elif 400 < event.x <= 500 and y_range_start < event.y < y_range_end:
                self.game.move_piece((self.selected_pos, self.promotion_to_square, 5*self.game.turn.value))
            
            self.selected_pos = None
            self.show_promotion = False
            self.promotion_piece = None
            self.promotion_to_square = None
            self.print_game()
            self.clicked.set(True)
            return
        # If below the board, do nothing
        if event.y > self.board_size + self.info_size:
            self.clicked.set(True)
            return
        elif event.y < self.info_size:
            # If clicked on the reset button
            if self.board_size - 100 < event.x < self.board_size and (self.player_info_size // 2) + self.game_info_size - 20 < event.y < (self.player_info_size // 2) + self.game_info_size + 20:
                print("Game reset")
                self.game.reset_board()
            self.selected_pos = None
            self.print_game()
            self.clicked.set(True)
            return
        col = event.x // self.square_size
        row = (event.y - self.info_size) // self.square_size # Account for the space above the board
        print(f"Clicked on {row}, {col}")
        if self.selected_pos is not None:
            piece = self.game.board[self.selected_pos]
            # If attempting promotion
            if (piece == 1 and row == 0) or (piece == -1 and row == 7):
                promotion_move = (self.selected_pos, (row, col), 5 * self.game.turn.value)
                if promotion_move in self.game.get_legal_moves(self.selected_pos):
                    # If promotion legal
                    self.show_promotion = True
                    self.promotion_to_square = (row, col)
            else:
                move = (self.selected_pos, (row, col), piece)   # TODO: Update this to be whatever piece chosen by user in case of pawn promotion
                if move in self.game.get_legal_moves(self.selected_pos):
                    self.game.move_piece(move)
                self.selected_pos = None
        elif self.game.board[row][col] * self.game.turn.value > 0:
            self.selected_pos = (row, col)
        else:
            self.selected_pos = None
            self.clicked.set(True)
            return
        
        self.print_game()
        self.clicked.set(True)

    def get_shade_image(self):
        # Create a new image with the same size as the canvas
        image = Image.new('RGBA', (self.board_size, self.board_size + self.info_size + self.player_info_size))

        # Draw a semi-transparent black rectangle on the image
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), image.size], fill=(0, 0, 0, 128))  # RGBA color

        # Convert the PIL image to a PhotoImage
        photo = ImageTk.PhotoImage(image)
        return photo