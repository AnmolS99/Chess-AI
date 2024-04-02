from pieces.piece import Piece


class Bishop(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, color_value):
        moves = []
        x, y = pos
        # Diagonally down-right
        for i in range(1, 8 - max(x, y)):
            if board[x + i][y + i] == 0:
                moves.append((x + i, y + i))
            elif board[x + i][y + i] * color_value < 0:
                moves.append((x + i, y + i))
                break
            else:
                break
        # Diagonally down-left
        for i in range(1, 8 - max(x, 7 - y)):
            if board[x + i][y - i] == 0:
                moves.append((x + i, y - i))
            elif board[x + i][y - i] * color_value < 0:
                moves.append((x + i, y - i))
                break
            else:
                break
        # Diagonally up-right
        for i in range(1, 8 - max(7 - x, y)):
            if board[x - i][y + i] == 0:
                moves.append((x - i, y + i))
            elif board[x - i][y + i] * color_value < 0:
                moves.append((x - i, y + i))
                break
            else:
                break
        # Diagonally up-left
        for i in range(1, 8 - max(7 - x, 7 - y)):
            if board[x - i][y - i] == 0:
                moves.append((x - i, y - i))
            elif board[x - i][y - i] * color_value < 0:
                moves.append((x - i, y - i))
                break
            else:
                break
        
        return moves