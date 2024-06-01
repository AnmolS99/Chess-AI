from move import Move
from player import Player
from pieces.piece import Piece

piece_int = 1
promotion_pieces = [2, 3, 4, 5]
class Pawn(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        piece_value = piece_int * color_value
        promotion_pieces_value = [piece * color_value for piece in promotion_pieces]
        moves = []
        x, y = pos
        if color_value == Player.white.value:
            start = 6
            pro_promotion = 1
            forward = (x - 1, y)
            double_forward = (x - 2, y)
            forward_left = (x - 1, y - 1)
            forward_right = (x - 1, y + 1)
        else:
            start = 1
            pro_promotion = 6
            forward = (x + 1, y)
            double_forward = (x + 2, y)
            forward_left = (x + 1, y - 1)
            forward_right = (x + 1, y + 1)
        if x == start:
            if board[forward] == 0:
                moves.append(Move(pos, forward, piece_value))
                if board[double_forward] == 0:
                    moves.append(Move(pos, double_forward, piece_value))
        else:
            if board[forward] == 0:
                if x == pro_promotion:
                    for promotion_piece in promotion_pieces_value:
                        moves.append(Move(pos, forward, promotion_piece, promotion=True))    
                else:
                    moves.append(Move(pos, forward, piece_value))
        if y > 0 and board[forward_left] * color_value < 0:
            if x == pro_promotion:
                for promotion_piece in promotion_pieces_value:
                    moves.append(Move(pos, forward_left, promotion_piece, promotion=True))    
            else:
                moves.append(Move(pos, forward_left, piece_value))
        if y < 7 and board[forward_right] * color_value < 0:
            if x == pro_promotion:
                for promotion_piece in promotion_pieces_value:
                    moves.append(Move(pos, forward_right, promotion_piece, promotion=True))    
            else:
                moves.append(Move(pos, forward_right, piece_value))
        if possible_en_passant is not None:
            if board[possible_en_passant] == -piece_value and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                moves.append(Move(pos, (possible_en_passant[0] - color_value, possible_en_passant[1]), piece_value))
        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, possible_en_passant, color_value):
        piece_value = piece_int * color_value
        capture_moves = []
        x, y = pos
        if color_value == Player.white.value:
            if y > 0:
                capture_moves.append(Move(pos, (x - 1, y - 1), piece_value))
            if y < 7:
                capture_moves.append(Move(pos, (x - 1, y + 1), piece_value))
        else:
            if y > 0:
                capture_moves.append(Move(pos, (x + 1, y - 1), piece_value))
            if y < 7:
                capture_moves.append(Move(pos, (x + 1, y + 1), piece_value))

        return capture_moves