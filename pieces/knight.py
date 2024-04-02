from pieces.piece import Piece
from player import Player


class Knight(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, color_value):
        moves = []
        x, y = pos
        if color_value == Player.white.value:
            if x > 1:
                if y > 0 and board[x - 2][y - 1] <= 0:
                    moves.append((x - 2, y - 1))
                if y < 7 and board[x - 2][y + 1] <= 0:
                    moves.append((x - 2, y + 1))
            if x > 0:
                if y > 1 and board[x - 1][y - 2] <= 0:
                    moves.append((x - 1, y - 2))
                if y < 6 and board[x - 1][y + 2] <= 0:
                    moves.append((x - 1, y + 2))
            if x < 6:
                if y > 0 and board[x + 2][y - 1] <= 0:
                    moves.append((x + 2, y - 1))
                if y < 7 and board[x + 2][y + 1] <= 0:
                    moves.append((x + 2, y + 1))
            if x < 7:
                if y > 1 and board[x + 1][y - 2] <= 0:
                    moves.append((x + 1, y - 2))
                if y < 6 and board[x + 1][y + 2] <= 0:
                    moves.append((x + 1, y + 2))
        else:
            if x > 1:
                if y > 0 and board[x - 2][y - 1] >= 0:
                    moves.append((x - 2, y - 1))
                if y < 7 and board[x - 2][y + 1] >= 0:
                    moves.append((x - 2, y + 1))
            if x > 0:
                if y > 1 and board[x - 1][y - 2] >= 0:
                    moves.append((x - 1, y - 2))
                if y < 6 and board[x - 1][y + 2] >= 0:
                    moves.append((x - 1, y + 2))
            if x < 6:
                if y > 0 and board[x + 2][y - 1] >= 0:
                    moves.append((x + 2, y - 1))
                if y < 7 and board[x + 2][y + 1] >= 0:
                    moves.append((x + 2, y + 1))
            if x < 7:
                if y > 1 and board[x + 1][y - 2] >= 0:
                    moves.append((x + 1, y - 2))
                if y < 6 and board[x + 1][y + 2] >= 0:
                    moves.append((x + 1, y + 2))
        return moves