import copy
import numpy as np
from player import Player
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

board_positions = [(row, col) for row in range(8) for col in range(8)]
piece_dict = {1: Pawn, 2: Rook, 3: Knight, 4: Bishop, 5: Queen, 6: King}
piece_value = {1: 1, 2: 5, 3: 3, 4: 3, 5: 9}

class ChessBoard:

    
    def reset_board(self):
        self.board = np.array([
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 3, 4, 5, 6, 4, 3, 2]
            ])

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
                hyp_board, hyp_king_position = self.hyp_move_piece(self.board.copy(), self.king_position.copy(), move, self.turn)
                if not self.is_in_check(hyp_board, self.turn, hyp_king_position):
                    legal_moves.append(move)
        return legal_moves
    
    """Returns all legals moves for a player"""
    def get_all_legal_moves(self):
        all_legal_moves = []
        for pos in board_positions:
            if self.board[pos] * self.turn.value > 0:
                all_legal_moves.extend(self.get_legal_moves(pos))
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
            return piece_dict[abs(selected_piece)].get_moves(board, selected_pos, possible_en_passant, castling_rights, self.get_all_possible_capture_moves(self.board, -self.turn.value), color_value)
    
    """Returns all possible capture moves for a selected piece (in a position). NOTE that this function does not check if the move puts the king in check."""
    def get_possible_capture_moves(self, selected_pos, board=None, color_value=None, ignore_turn=False):
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
            return piece_dict[abs(selected_piece)].get_capture_moves(board, selected_pos, color_value)
    
    """Returns all possible moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def get_all_possible_moves(self, board, color_value, possible_en_passant):
        all_possible_moves = []
        for pos in board_positions:
            if board[pos] * color_value > 0:
                all_possible_moves.extend(self.get_possible_moves(pos, board, color_value, possible_en_passant, ignore_turn=True))
        return all_possible_moves
    
    """Returns all possible capture moves for a player. NOTE that this function does not check if the move puts the king in check."""
    def get_all_possible_capture_moves(self, board, color_value):
        all_possible_capture_moves = []
        for pos in board_positions:
            if board[pos] * color_value > 0:
                    all_possible_capture_moves.extend(self.get_possible_capture_moves(pos, board, color_value, ignore_turn=True))
        return all_possible_capture_moves
    
    def is_in_check(self, board, turn, king_position=None):
        if king_position is None:
            king_pos = self.king_position[turn]
        else:
            king_pos = king_position[turn]
        if king_pos is not None:
            return king_pos in [end_pos for (start_pos, end_pos, piece) in self.get_all_possible_capture_moves(board, -turn.value)]
        return False
    
    def is_checkmate(self):
        return self.is_in_check(self.board, self.turn) and len(self.get_all_legal_moves()) == 0
    
    def is_stalemate(self):
        return (not self.is_in_check(self.board, self.turn)) and len(self.get_all_legal_moves()) == 0
    
    def is_dead_position(self):
        return np.count_nonzero(self.board == -6) == 1 and np.count_nonzero(self.board == 6) == 1 and np.count_nonzero(self.board != 0) == 2
    
    def move_piece(self, move):
        start_pos, end_pos, piece = move
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
    
    def hyp_move_piece(self, board, king_position, move, turn):
        start_pos, end_pos, piece = move
        board[start_pos] = 0
        if abs(piece) == 1 and board[end_pos] == 0 and start_pos[1] != end_pos[1]:
            board[(start_pos[0], end_pos[1])] = 0
        board[end_pos] = piece
        if abs(piece) == 6:
            king_position[turn] = end_pos
            # If king moves two places, it is castling
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
                
        return board, king_position
    
    def get_points(self):
        """
        Returns a dictionary of both Players points, relative to each other. 
        Example: If both players have captured equal material, except white has an extra rook,
        white will have +5 points, while black will have -5.
        """
        white_points = 0
        black_points = 0
        for row in self.board:
            for piece in row:
                if abs(piece) > 5:
                    pass
                elif piece > 0:
                    white_points += piece_value[abs(piece)]
                elif piece < 0:
                    black_points += piece_value[abs(piece)]
        return {Player.white: white_points - black_points, Player.black: black_points - white_points}
    
    def copy(self):
        new_board = ChessBoard()
        new_board.board = copy.deepcopy(self.board)
        new_board.turn = self.turn
        new_board.captured_pieces = copy.deepcopy(self.captured_pieces)
        new_board.king_position = copy.deepcopy(self.king_position)
        new_board.possible_en_passant = self.possible_en_passant
        new_board.castling_rights = copy.deepcopy(self.castling_rights)
        return new_board