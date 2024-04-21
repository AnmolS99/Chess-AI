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
        promotion_pieces_value = promotion_pieces * color_value
        moves = []
        x, y = pos
        if color_value == Player.white.value:
            if x == 6:
                if board[x - 1][y] == 0:
                    moves.append(Move(pos, (x - 1, y), piece_value))
                    if board[x - 2][y] == 0:
                        moves.append(Move(pos, (x - 2, y), piece_value))
            else:
                if board[x - 1][y] == 0:
                    if x == 1:
                        for promotion_piece in promotion_pieces_value:
                            moves.append(Move(pos, (x - 1, y), promotion_piece))    
                    else:
                        moves.append(Move(pos, (x - 1, y), piece_value))
            if y > 0 and board[x - 1][y - 1] < 0:
                if x == 1:
                    for promotion_piece in promotion_pieces_value:
                        moves.append(Move(pos, (x - 1, y - 1), promotion_piece))    
                else:
                    moves.append(Move(pos, (x - 1, y - 1), piece_value))
            if y < 7 and board[x - 1][y + 1] < 0:
                if x == 1:
                    for promotion_piece in promotion_pieces_value:
                        moves.append(Move(pos, (x - 1, y + 1), promotion_piece))    
                else:
                    moves.append(Move(pos, (x - 1, y + 1), piece_value))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == -1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    moves.append(Move(pos, (possible_en_passant[0] - 1, possible_en_passant[1]), piece_value))
            
        else:
            if x == 1:
                if board[x + 1][y] == 0:
                    moves.append(Move(pos, (x + 1, y), piece_value))
                    if board[x + 2][y] == 0:
                        moves.append(Move(pos, (x + 2, y), piece_value))
            else:
                if board[x + 1][y] == 0:
                    if x == 6:
                        for promotion_piece in promotion_pieces_value:
                            moves.append(Move(pos, (x + 1, y), promotion_piece))    
                    else:
                        moves.append(Move(pos, (x + 1, y), piece_value))
            if y > 0 and board[x + 1][y - 1] > 0:
                if x == 6:
                    for promotion_piece in promotion_pieces_value:
                        moves.append(Move(pos, (x + 1, y - 1), promotion_piece))    
                else:
                    moves.append(Move(pos, (x + 1, y - 1), piece_value))
            if y < 7 and board[x + 1][y + 1] > 0:
                if x == 6:
                    for promotion_piece in promotion_pieces_value:
                        moves.append(Move(pos, (x + 1, y + 1), promotion_piece))    
                else:
                    moves.append(Move(pos, (x + 1, y + 1), piece_value))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == 1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    moves.append(Move(pos, (possible_en_passant[0] + 1, possible_en_passant[1]), piece_value))
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
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == -1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    capture_moves.append(Move(pos, (possible_en_passant[0] - 1, possible_en_passant[1]), piece_value))
            
        else:
            if y > 0:
                capture_moves.append(Move(pos, (x + 1, y - 1), piece_value))
            if y < 7:
                capture_moves.append(Move(pos, (x + 1, y + 1), piece_value))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == 1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    capture_moves.append(Move(pos, (possible_en_passant[0] + 1, possible_en_passant[1]), piece_value))

        return capture_moves