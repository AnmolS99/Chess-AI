from pieces.bishop import Bishop
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
                moves.append((pos, (i, y), piece_value))
            elif board[i][y] * color_value < 0:
                moves.append((pos, (i, y), piece_value))
                break
            else:
                break
        # Up
        for i in range (x - 1, -1, -1):
            if board[i][y] == 0:
                moves.append((pos, (i, y), piece_value))
            elif board[i][y] * color_value < 0:
                moves.append((pos, (i, y), piece_value))
                break
            else:
                break
        # Right
        for i in range (y + 1, 8):
            if board[x][i] == 0:
                moves.append((pos, (x, i), piece_value))
            elif board[x][i] * color_value < 0:
                moves.append((pos, (x, i), piece_value))
                break
            else:
                break
        # Left
        for i in range (y - 1, -1, -1):
            if board[x][i] == 0:
                moves.append((pos, (x, i), piece_value))
            elif board[x][i] * color_value < 0:
                moves.append((pos, (x, i), piece_value))
                break
            else:
                break
        
        # Diagonally down-right
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, 1, 1, x, y)
        # Diagonally down-left
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, 1, -1, x, 7 - y)
        # Diagonally up-right
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, -1, 1, 7 - x, y)
        # Diagonally up-left
        Bishop.diagonal_moves(board, moves, pos, piece_value, color_value, -1, -1, 7 - x, 7 - y)

        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, color_value):
        return Queen.get_moves(board, pos, None, None, None, color_value)