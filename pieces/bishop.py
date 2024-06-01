from move import Move
from pieces.piece import Piece


piece_int = 4

class Bishop(Piece):

    
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        piece_value = piece_int * color_value
        moves = []
        x, y = pos
        # Diagonally down-right
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, 1, 1, x, y)
        # Diagonally down-left
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, 1, -1, x, 7 - y)
        # Diagonally up-right
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, -1, 1, 7 - x, y)
        # Diagonally up-left
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, -1, -1, 7 - x, 7 - y)
        return moves
    
    @staticmethod
    def diagonal_moves(board, moves, pos, piece_value, color_value, x_diag_direction, y_diag_direction, x_direction_dist, y_direction_dist):
        """
        x_direction_dist: The x (row) distance gone in the diagonal directon (this will be different if you go diagonally up or down)
        y_direction_dist: The y (col) distance gone in the diagonal directon (this will be different if you go diagonally left or right)
        """
        i = 1
        x, y = pos
        while i < 8 - max(x_direction_dist, y_direction_dist):
            diag_pos = (x + (i * x_diag_direction), y + (i * y_diag_direction))
            diag_pos_val = board[diag_pos]
            if diag_pos_val == 0:
                moves.append(Move(pos, diag_pos, piece_value))
            elif diag_pos_val * color_value < 0:
                moves.append(Move(pos, diag_pos, piece_value))
                break
            else:
                break
            i += 1
    
    @staticmethod
    def get_capture_moves(board, pos, color_value):
        return Bishop.get_moves(board, pos, None, None, None, color_value)