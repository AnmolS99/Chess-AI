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
        for i in range(1, 8 - max(x, y)):
            if board[x + i][y + i] == 0:
                moves.append(Move(pos, (x + i, y + i), piece_value))
            elif board[x + i][y + i] * color_value < 0:
                moves.append(Move(pos, (x + i, y + i), piece_value))
                break
            else:
                break
        # Diagonally down-left
        for i in range(1, 8 - max(x, 7 - y)):
            if board[x + i][y - i] == 0:
                moves.append(Move(pos, (x + i, y - i), piece_value))
            elif board[x + i][y - i] * color_value < 0:
                moves.append(Move(pos, (x + i, y - i), piece_value))
                break
            else:
                break
        # Diagonally up-right
        for i in range(1, 8 - max(7 - x, y)):
            if board[x - i][y + i] == 0:
                moves.append(Move(pos, (x - i, y + i), piece_value))
            elif board[x - i][y + i] * color_value < 0:
                moves.append(Move(pos, (x - i, y + i), piece_value))
                break
            else:
                break
        # Diagonally up-left
        for i in range(1, 8 - max(7 - x, 7 - y)):
            if board[x - i][y - i] == 0:
                moves.append(Move(pos, (x - i, y - i), piece_value))
            elif board[x - i][y - i] * color_value < 0:
                moves.append(Move(pos, (x - i, y - i), piece_value))
                break
            else:
                break
        
        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, possible_en_passant, color_value):
        return Bishop.get_moves(board, pos, possible_en_passant, None, None, color_value)