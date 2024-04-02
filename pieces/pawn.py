from player import Player
from pieces.piece import Piece


class Pawn(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, color_value):
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
            # En passant needs to be implemented
            
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
            # En passant needs to be implemented
        return moves