import copy
import numpy as np
from move import Move
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
        self.castling_rights = {Player.white: {"king_side": True, "queen_side": True}, Player.black: {"king_side": True, "queen_side": True}}
    
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
        self.possible_en_passant = None
        self.castling_rights = {Player.white: {"king_side": True, "queen_side": True}, Player.black: {"king_side": True, "queen_side": True}}

    """Returns all legals moves for a selected piece (in a position)"""
    def get_legal_moves(self, selected_pos):
        legal_moves = []
        if self.board[selected_pos] * self.turn.value > 0:
            for move in self.get_possible_moves(selected_pos):
                hypotetical_board, hypotetical_king_position, hypotetical_en_passant = self.hypotetical_move_piece(self.board.copy(), self.king_position.copy(), move, self.turn)
                if not self.is_in_check(hypotetical_board, self.turn, hypotetical_king_position, hypotetical_en_passant):
                    legal_moves.append(move)
        return legal_moves
    
    """Returns all legals moves for a player"""
    def get_all_legal_moves(self):
        all_legal_moves = []
        for row in range(8):
            for col in range(8):    # Maybe change these two for-loops to one that only look at the positions of the current players pieces
                if self.board[row][col] * self.turn.value > 0:
                    all_legal_moves.extend(self.get_legal_moves((row, col)))
        return all_legal_moves
    
    """Returns all possible moves for a selected piece (in a position). NOTE that this function does not check if the move puts the king in check."""
    def get_possible_moves(self, selected_pos, board=None, color_value=None, possible_en_passant=None, castling_rights=None, ignore_turn=False):
        if color_value is None:
            color_value = self.turn.value
        if board is None:
            board = self.board
        if possible_en_passant is None:
            possible_en_passant = self.possible_en_passant
        if castling_rights is None:
            castling_rights = self.castling_rights
        selected_piece = board[selected_pos]
        if selected_piece == 0:
            return []
        elif not ignore_turn and color_value * selected_piece < 0:
            return []
        else:
            return piece_dict[abs(selected_piece)].get_moves(board, selected_pos, possible_en_passant, castling_rights, self.get_all_possible_capture_moves(self.board, -self.turn.value, self.possible_en_passant), color_value)
    
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
            for col in range(8): # Maybe change these two for-loops to one that only look at the positions of the current players pieces
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
            return king_pos in [move.end_pos for move in self.get_all_possible_capture_moves(board, -turn.value, en_passant)]
        return False
    
    def is_checkmate(self):
        return self.is_in_check(self.board, self.turn) and len(self.get_all_legal_moves()) == 0
    
    def is_stalemate(self):
        return (not self.is_in_check(self.board, self.turn)) and len(self.get_all_legal_moves()) == 0
    
    def is_dead_position(self):
        return np.count_nonzero(self.board == -6) == 1 and np.count_nonzero(self.board == 6) == 1 and np.count_nonzero(self.board != 0) == 2
    
    def move_piece(self, move: Move):
        start_pos = move.start_pos
        end_pos = move.end_pos
        piece = move.end_piece
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
            # If king moves to places, it is castling
            if abs(start_pos[1] - end_pos[1]) == 2:
                if (abs(end_pos[1]) == 2):
                    # Move queen side rook
                    rook_piece = self.board[(end_pos[0], 0)]
                    self.board[(end_pos[0], 0)] = 0
                    self.board[(end_pos[0], 3)] = rook_piece
                elif (abs(end_pos[1]) == 6):
                    # Move king side rook
                    rook_piece = self.board[(end_pos[0], 7)]
                    self.board[(end_pos[0], 7)] = 0
                    self.board[(end_pos[0], 5)] = rook_piece
                
            # Remove all castling rights
            self.castling_rights[self.turn]["king_side"] = False
            self.castling_rights[self.turn]["queen_side"] = False
        
        # If rook moves, remove castling rights
        if abs(piece) == 2:
            if (self.turn == Player.white and start_pos == (7, 0)) or (self.turn == Player.black and start_pos == (0, 0)):
                self.castling_rights[self.turn]["queen_side"] = False
            elif (self.turn == Player.white and start_pos == (7, 7)) or (self.turn == Player.black and start_pos == (0, 7)):
                self.castling_rights[self.turn]["king_side"] = False


        # If pawn moves two squares, update possible en passant square
        if abs(piece) == 1 and abs(start_pos[0] - end_pos[0]) == 2:
            self.possible_en_passant = end_pos
        else:
            self.possible_en_passant = None
        self.turn = Player.white if self.turn == Player.black else Player.black
    
    def hypotetical_move_piece(self, board, king_position, move: Move, turn):
        start_pos = move.start_pos
        end_pos = move.end_pos
        piece = move.end_piece
        board[start_pos] = 0
        if abs(piece) == 1 and board[end_pos] == 0 and start_pos[1] != end_pos[1]:
            board[(start_pos[0], end_pos[1])] = 0
        board[end_pos] = piece
        if abs(piece) == 6:
            king_position[turn] = end_pos
            # If king moves to places, it is castling
            if abs(start_pos[1] - end_pos[1]) == 2:
                if (abs(end_pos[1]) == 2):
                    # Move queen side rook
                    rook_piece = board[(end_pos[0], 0)]
                    board[(end_pos[0], 0)] = 0
                    board[(end_pos[0], 3)] = rook_piece
                elif (abs(end_pos[1]) == 6):
                    # Move king side rook
                    rook_piece = board[(end_pos[0], 7)]
                    board[(end_pos[0], 7)] = 0
                    board[(end_pos[0], 5)] = rook_piece
                
        if abs(piece) == 1 and abs(start_pos[0] - end_pos[0]) == 2:
            possible_en_passant = end_pos
        else:
            possible_en_passant = None
        return board, king_position, possible_en_passant
    
    def copy(self):
        new_board = copy.deepcopy(ChessBoard())
        new_board.board = copy.deepcopy(self.board)
        new_board.turn = copy.deepcopy(self.turn)
        new_board.captured_pieces = copy.deepcopy(self.captured_pieces)
        new_board.king_position = copy.deepcopy(self.king_position)
        new_board.possible_en_passant = copy.deepcopy(self.possible_en_passant)
        new_board.castling_rights = copy.deepcopy(self.castling_rights)
        return new_board