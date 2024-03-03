from pieces.piece import Piece

class Rook(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, color):
        moves = []
        x, y = pos
        # Down
        for i in range (x + 1, 8):
            if board[i][y] == 0:
                moves.append((i, y))
            elif board[i][y] * color.value < 0:
                moves.append((i, y))
                break
            else:
                break
        # Up
        for i in range (x - 1, -1, -1):
            if board[i][y] == 0:
                moves.append((i, y))
            elif board[i][y] * color.value < 0:
                moves.append((i, y))
                break
            else:
                break
        # Right
        for i in range (y + 1, 8):
            if board[x][i] == 0:
                moves.append((x, i))
            elif board[x][i] * color.value < 0:
                moves.append((x, i))
                break
            else:
                break
        # Left
        for i in range (y - 1, -1, -1):
            if board[x][i] == 0:
                moves.append((x, i))
            elif board[x][i] * color.value < 0:
                moves.append((x, i))
                break
            else:
                break

        return moves