from pieces.piece import Piece
from player import Player

piece_int = 6

class King(Piece):
    
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        piece_value = piece_int * color_value
        moves = []
        x, y = pos
        if x > 0:
            # Up
            if board[x - 1][y] * color_value <= 0:
                moves.append((pos, (x - 1, y), piece_value))
            
            # Up-left
            if y > 0:
                if board[x - 1][y - 1] * color_value <= 0:
                    moves.append((pos, (x - 1, y - 1), piece_value))
            
            # Up-right
            if y < 7:
                if board[x - 1][y + 1] * color_value <= 0:
                    moves.append((pos, (x - 1, y + 1), piece_value))
        
        if y > 0:

            # Left
            if board[x][y - 1] * color_value <= 0:
                    moves.append((pos, (x, y - 1), piece_value))
        
        if y < 7:

            # Right
            if board[x][y + 1] * color_value <= 0:
                    moves.append((pos, (x, y + 1), piece_value))

        if x < 7:
            # Down
            if board[x + 1][y] * color_value <= 0:
                moves.append((pos, (x + 1, y), piece_value))
            
            # Down-left
            if y > 0:
                if board[x + 1][y - 1] * color_value <= 0:
                    moves.append((pos, (x + 1, y - 1), piece_value))
            
            # Down-right
            if y < 7:
                if board[x + 1][y + 1] * color_value <= 0:
                    moves.append((pos, (x + 1, y + 1), piece_value))
        
        if opp_capture_moves is not None and (x, y) not in [end_pos for (_, end_pos, _) in opp_capture_moves]:    # King cannot castle while in check 
            white_king_side_squares = [(7, 5), (7, 6)]
            white_queen_side_squares = [(7, 2), (7, 3), (7, 4)]
            black_king_side_squares = [(0, 5), (0, 6)]
            black_queen_side_squares = [(0, 2), (0, 3), (0, 4)]
            # Castling (white)
            if color_value == Player.white.value:

                # Queen side
                if castling_rights[Player.white]["queen_side"] and all(square == 0 for square in board[7][1:4]) and board[7][0] == 2 and not any(square in white_queen_side_squares for square in [end_pos for (_, end_pos, _) in opp_capture_moves]):
                    moves.append((pos, (7, 2), piece_value))
                
                # King side
                if castling_rights[Player.white]["king_side"] and all(square == 0 for square in board[7][5:7]) and board[7][7] == 2 and not any(square in white_king_side_squares for square in [end_pos for (_, end_pos, _) in opp_capture_moves]):
                    moves.append((pos, (7, 6), piece_value))
            
            # Castling (black)
            if color_value == Player.black.value:

                # King side
                if castling_rights[Player.black]["queen_side"] and all(square == 0 for square in board[0][1:4]) and board[0][0] == -2 and not any(square in black_queen_side_squares for square in [end_pos for (_, end_pos, _) in opp_capture_moves]):
                    moves.append((pos, (0, 2), piece_value))
                
                # Queen side
                if castling_rights[Player.black]["king_side"] and all(square == 0 for square in board[0][5:7]) and board[0][7] == -2 and not any(square in black_king_side_squares for square in [end_pos for (_, end_pos, _) in opp_capture_moves]):
                    moves.append((pos, (0, 6), piece_value))

        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, color_value):
        return King.get_moves(board, pos, None, None, None, color_value)