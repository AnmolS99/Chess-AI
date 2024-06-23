from pieces.piece import Piece

piece_int = 2

class Rook(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        piece_value = piece_int * color_value
        moves = []
        x, y = pos
        # Down
        for i in range (x + 1, 8):
            if board[i][y] == 0:
                moves.append((pos, (i, y), piece_value, False))
            elif board[i][y] * color_value < 0:
                moves.append((pos, (i, y), piece_value, True))
                break
            else:
                break
        # Up
        for i in range (x - 1, -1, -1):
            if board[i][y] == 0:
                moves.append((pos, (i, y), piece_value, False))
            elif board[i][y] * color_value < 0:
                moves.append((pos, (i, y), piece_value, True))
                break
            else:
                break
        # Right
        for i in range (y + 1, 8):
            if board[x][i] == 0:
                moves.append((pos, (x, i), piece_value, False))
            elif board[x][i] * color_value < 0:
                moves.append((pos, (x, i), piece_value, True))
                break
            else:
                break
        # Left
        for i in range (y - 1, -1, -1):
            if board[x][i] == 0:
                moves.append((pos, (x, i), piece_value, False))
            elif board[x][i] * color_value < 0:
                moves.append((pos, (x, i), piece_value, True))
                break
            else:
                break

        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, color_value):
        return Rook.get_moves(board, pos, None, None, None, color_value)