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

    """Returns all legals moves for a selected piece (in a position)"""
    def get_legal_moves(self, selected_pos):
        legal_moves = []
        if self.board[selected_pos] * self.turn.value > 0:
            for move in self.get_possible_moves(selected_pos):
                hypotetical_board, hypotetical_king_position = self.hypotetical_move_piece(self.board.copy(), self.king_position.copy(), selected_pos, move, self.turn)
                if not self.is_in_check(hypotetical_board, self.turn, hypotetical_king_position):
                    legal_moves.append(move)
        return legal_moves
    
    """Returns all possible moves for a selected piece (in a position). NOTE that this function does not check if the move puts the king in check."""
    def get_possible_moves(self, selected_pos, board=None, color_value=None, ignore_turn=False):
        if color_value is None:
            color_value = self.turn.value
        if board is None:
            board = self.board
        selected_piece = board[selected_pos]
        if selected_piece == 0:
            return []
        elif not ignore_turn and color_value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_moves(board, selected_pos, color_value)
    
    """Returns all possible moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def get_all_possible_moves(self, board, color_value):
        all_possible_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] * color_value > 0:
                    all_possible_moves.extend(self.get_possible_moves((row, col), board, color_value, ignore_turn=True))
        return all_possible_moves
    
    """Returns all possible moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def is_in_check(self, board, turn, king_position=None):
        if king_position is None:
            king_pos = self.king_position[turn]
        else:
            king_pos = king_position[turn]
        if king_pos is not None:
            return king_pos in self.get_all_possible_moves(board, -turn.value)
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
    
    def hypotetical_move_piece(self, board, king_position, start_pos, end_pos, turn):
        piece = self.board[start_pos]
        board[end_pos] = board[start_pos]
        board[start_pos] = 0
        if abs(piece) == 6:
            king_position[turn] = end_pos
        return board, king_position