from move import Move
from pieces.piece import Piece

piece_int = 5

class Queen(Piece):
    
    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        piece_value = piece_int * color_value
        moves = []
        x, y = pos
        # Down
        for i in range (x + 1, 8):
            if board[i][y] == 0:
                moves.append(Move(pos, (i, y), piece_value))
            elif board[i][y] * color_value < 0:
                moves.append(Move(pos, (i, y), piece_value))
                break
            else:
                break
        # Up
        for i in range (x - 1, -1, -1):
            if board[i][y] == 0:
                moves.append(Move(pos, (i, y), piece_value))
            elif board[i][y] * color_value < 0:
                moves.append(Move(pos, (i, y), piece_value))
                break
            else:
                break
        # Right
        for i in range (y + 1, 8):
            if board[x][i] == 0:
                moves.append(Move(pos, (x, i), piece_value))
            elif board[x][i] * color_value < 0:
                moves.append(Move(pos, (x, i), piece_value))
                break
            else:
                break
        # Left
        for i in range (y - 1, -1, -1):
            if board[x][i] == 0:
                moves.append(Move(pos, (x, i), piece_value))
            elif board[x][i] * color_value < 0:
                moves.append(Move(pos, (x, i), piece_value))
                break
            else:
                break
        
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
        return Queen.get_moves(board, pos, possible_en_passant, None, None, color_value)