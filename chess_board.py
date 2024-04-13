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
        self.possible_en_passant = None
    
    def reset_board(self):
        # Reset white pieces
        self.board[6][:] = np.ones(8)
        self.board[7][:] = np.array([2, 3, 4, 5, 6, 4, 3, 2])

        # This one-liner sets rows 2 to 5 to 0
        self.board[2:6][:] = 0
        
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
                hypotetical_board, hypotetical_king_position, hypotetical_en_passant = self.hypotetical_move_piece(self.board.copy(), self.king_position.copy(), selected_pos, move, self.turn)
                if not self.is_in_check(hypotetical_board, self.turn, hypotetical_king_position, hypotetical_en_passant):
                    legal_moves.append(move)
        return legal_moves
    
    """Returns all legals moves for a player"""
    def get_all_legal_moves(self):
        all_legal_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] * self.turn.value > 0:
                    all_legal_moves.extend(self.get_legal_moves((row, col)))
        return all_legal_moves
    
    """Returns all possible moves for a selected piece (in a position). NOTE that this function does not check if the move puts the king in check."""
    def get_possible_moves(self, selected_pos, board=None, color_value=None, possible_en_passant=None, ignore_turn=False):
        if color_value is None:
            color_value = self.turn.value
        if board is None:
            board = self.board
        if possible_en_passant is None:
            possible_en_passant = self.possible_en_passant
        selected_piece = board[selected_pos]
        if selected_piece == 0:
            return []
        elif not ignore_turn and color_value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_moves(board, selected_pos, possible_en_passant, color_value)
    
    """Returns all possible capture moves for a selected piece (in a position). NOTE that this function does not check if the move puts the king in check."""
    def get_possible_capture_moves(self, selected_pos, board=None, color_value=None, possible_en_passant=None, ignore_turn=False):
        if color_value is None:
            color_value = self.turn.value
        if board is None:
            board = self.board
        if possible_en_passant is None:
            possible_en_passant = self.possible_en_passant
        selected_piece = board[selected_pos]
        if selected_piece == 0:
            return []
        elif not ignore_turn and color_value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_capture_moves(board, selected_pos, possible_en_passant, color_value)
    
    """Returns all possible moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def get_all_possible_moves(self, board, color_value, possible_en_passant):
        all_possible_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] * color_value > 0:
                    all_possible_moves.extend(self.get_possible_moves((row, col), board, color_value, possible_en_passant, ignore_turn=True))
        return all_possible_moves
    
    """Returns all possible capture moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def get_all_possible_capture_moves(self, board, color_value, possible_en_passant):
        all_possible_capture_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] * color_value > 0:
                    all_possible_capture_moves.extend(self.get_possible_capture_moves((row, col), board, color_value, possible_en_passant, ignore_turn=True))
        return all_possible_capture_moves
    
    def is_in_check(self, board, turn, king_position=None, possible_en_passant=None):
        if king_position is None:
            king_pos = self.king_position[turn]
        else:
            king_pos = king_position[turn]
        if possible_en_passant is None:
            en_passant = self.possible_en_passant
        else:
            en_passant = possible_en_passant
        if king_pos is not None:
            return king_pos in self.get_all_possible_capture_moves(board, -turn.value, en_passant)
        return False
    
    def is_checkmate(self):
        return self.is_in_check(self.board, self.turn) and len(self.get_all_legal_moves()) == 0
    
    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos]
        self.board[start_pos] = 0
        if self.board[end_pos] != 0:
            self.captured_pieces[self.turn].append(self.board[end_pos])
        elif abs(piece) == 1 and start_pos[1] != end_pos[1]:
            self.captured_pieces[self.turn].append(self.board[(start_pos[0], end_pos[1])])
            self.board[(start_pos[0], end_pos[1])] = 0
        self.board[end_pos] = piece
        # If king moves, update king position
        if abs(piece) == 6:
            self.king_position[self.turn] = end_pos
        # If pawn moves two squares, update possible en passant square
        if abs(piece) == 1 and abs(start_pos[0] - end_pos[0]) == 2:
            self.possible_en_passant = end_pos
        else:
            self.possible_en_passant = None
        self.turn = Player.white if self.turn == Player.black else Player.black
    
    def hypotetical_move_piece(self, board, king_position, start_pos, end_pos, turn):
        piece = self.board[start_pos]
        board[start_pos] = 0
        if abs(piece) == 1 and board[end_pos] == 0 and start_pos[1] != end_pos[1]:
            board[(start_pos[0], end_pos[1])] = 0
        board[end_pos] = board[start_pos]
        if abs(piece) == 6:
            king_position[turn] = end_pos
        if abs(piece) == 1 and abs(start_pos[0] - end_pos[0]) == 2:
            possible_en_passant = end_pos
        else:
            possible_en_passant = None
        return board, king_position, possible_en_passant