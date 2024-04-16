from player import Player
from pieces.piece import Piece


class Pawn(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        moves = []
        x, y = pos
        if color_value == Player.white.value:
            if x == 6:
                if board[x - 1][y] == 0:
                    moves.append((x - 1, y))
                    if board[x - 2][y] == 0:
                        moves.append((x - 2, y))
            else:
                if board[x - 1][y] == 0:
                    moves.append((x - 1, y))
            if y > 0 and board[x - 1][y - 1] < 0:
                moves.append((x - 1, y - 1))
            if y < 7 and board[x - 1][y + 1] < 0:
                moves.append((x - 1, y + 1))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == -1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    moves.append((possible_en_passant[0] - 1, possible_en_passant[1]))
            
        else:
            if x == 1:
                if board[x + 1][y] == 0:
                    moves.append((x + 1, y))
                    if board[x + 2][y] == 0:
                        moves.append((x + 2, y))
            else:
                if board[x + 1][y] == 0:
                    moves.append((x + 1, y))
            if y > 0 and board[x + 1][y - 1] > 0:
                moves.append((x + 1, y - 1))
            if y < 7 and board[x + 1][y + 1] > 0:
                moves.append((x + 1, y + 1))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == 1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    moves.append((possible_en_passant[0] + 1, possible_en_passant[1]))
        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, possible_en_passant, color_value):
        capture_moves = []
        x, y = pos
        if color_value == Player.white.value:
            if y > 0:
                capture_moves.append((x - 1, y - 1))
            if y < 7:
                capture_moves.append((x - 1, y + 1))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == -1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    capture_moves.append((possible_en_passant[0] - 1, possible_en_passant[1]))
            
        else:
            if y > 0:
                capture_moves.append((x + 1, y - 1))
            if y < 7:
                capture_moves.append((x + 1, y + 1))
            if possible_en_passant is not None:
                if board[possible_en_passant[0]][possible_en_passant[1]] == 1 and possible_en_passant[0] == x and (possible_en_passant[1] == y - 1 or possible_en_passant[1] == y + 1):
                    capture_moves.append((possible_en_passant[0] + 1, possible_en_passant[1]))
        return capture_moves