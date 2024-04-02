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
        self.king_position = {Player.white: (7, 4), Player.black: (0, 4)}
    
    def reset_board(self):
        # Reset white pieces
        self.board[6][:] = np.ones(8)
        self.board[7][:] = np.array([2, 3, 4, 5, 6, 4, 3, 2])
        
        # Reset black pieces
        self.board[1][:] = -np.ones(8)
        self.board[0][:] = -np.array([2, 3, 4, 5, 6, 4, 3, 2])

        self.turn = Player.white
        self.captured_pieces = {Player.white: [], Player.black: []}
        self.king_position = {Player.white: (7, 4), Player.black: (0, 4)}


    def get_legal_moves(self):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] * self.turn.value > 0:
                    for move in self.get_possible_moves((row, col)):
                        if not self.is_in_check(self.hypotetical_move_piece(self.board.copy(), (row, col), move), self.turn.value):
                            legal_moves.append(((row, col), move))
        return legal_moves
    
    """Returns all possible moves for a selected piece. NOTE that this function does not check if the move puts the king in check."""
    def get_possible_moves(self, selected_pos, color_value=None, ignore_turn=False):
        if color_value is None:
            color_value = self.turn.value
        selected_piece = self.board[selected_pos]
        if selected_piece == 0:
            return []
        elif not ignore_turn and color_value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_moves(self.board, selected_pos, color_value)
    
    def get_all_possible_moves(self, board, color_value):
        all_possible_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] * color_value > 0:
                    all_possible_moves.extend(self.get_possible_moves((row, col), color_value, ignore_turn=True))
        return all_possible_moves
        
    def is_in_check(self, board, color):
        king_pos = self.king_position[color]
        if king_pos is not None:
            return king_pos in self.get_all_possible_moves(board, -color.value)
        return False
    
    def hypotetical_is_in_check(self, board, color):
        king_pos = board.np.where(board == color.value * 6)
        if king_pos is not None:
            return king_pos in self.get_all_possible_moves(board, -color.value)
        return False
    
    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos]
        self.board[start_pos] = 0
        if self.board[end_pos] != 0:
            self.captured_pieces[self.turn].append(self.board[end_pos])
        self.board[end_pos] = piece
        if abs(piece) == 6:
            self.king_position[self.turn] = end_pos
        self.turn = Player.white if self.turn == Player.black else Player.black
    
    def hypotetical_move_piece(self, board, start_pos, end_pos):
        board[end_pos] = board[start_pos]
        board[start_pos] = 0
        return board