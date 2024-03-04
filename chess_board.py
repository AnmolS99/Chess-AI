import numpy as np
from player import Player
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

piece_dict = {1: Pawn, 2: Rook, 3: Knight, 4: Bishop, 5: Queen, 6: King}

class ChessBoard:

    def __init__(self):
        self.board = np.zeros((8, 8))   # np array is computationally more efficient than FEN notation and easier to program, however FEN is more memory efficient
        self.turn = Player.white
        self.captured_pieces = {Player.white: [], Player.black: []}
    
    def reset_board(self):
        # Reset white pieces
        self.board[6][:] = np.ones(8)
        self.board[7][:] = np.array([2, 3, 4, 5, 6, 4, 3, 2])
        
        # Reset black pieces
        self.board[1][:] = -np.ones(8)
        self.board[0][:] = -np.array([2, 3, 4, 5, 6, 4, 3, 2])

    
    def get_possible_moves(self, selected_pos):
        selected_piece = self.board[selected_pos]
        if selected_piece == 0:
            return []
        elif self.turn.value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_moves(self.board, selected_pos, self.turn)
    
    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos]
        self.board[start_pos] = 0
        if self.board[end_pos] != 0:
            self.captured_pieces[self.turn].append(self.board[end_pos])
        self.board[end_pos] = piece
        self.turn = Player.white if self.turn == Player.black else Player.black