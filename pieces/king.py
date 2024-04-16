from pieces.piece import Piece
from player import Player


class King(Piece):
    
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        moves = []
        x, y = pos
        if x > 0:
            # Up
            if board[x - 1][y] == 0 or board[x - 1][y] * color_value < 0:
                moves.append((x - 1, y))
            
            # Up-left
            if y > 0:
                if board[x - 1][y - 1] == 0 or board[x - 1][y - 1] * color_value < 0:
                    moves.append((x - 1, y - 1))
            
            # Up-right
            if y < 7:
                if board[x - 1][y + 1] == 0 or board[x - 1][y + 1] * color_value < 0:
                    moves.append((x - 1, y + 1))
        
        if y > 0:

            # Left
            if board[x][y - 1] == 0 or board[x][y - 1] * color_value < 0:
                    moves.append((x, y - 1))
        
        if y < 7:

            # Right
            if board[x][y + 1] == 0 or board[x][y + 1] * color_value < 0:
                    moves.append((x, y + 1))

        if x < 7:
            # Down
            if board[x + 1][y] == 0 or board[x + 1][y] * color_value < 0:
                moves.append((x + 1, y))
            
            # Down-left
            if y > 0:
                if board[x + 1][y - 1] == 0 or board[x + 1][y - 1] * color_value < 0:
                    moves.append((x + 1, y - 1))
            
            # Down-right
            if y < 7:
                if board[x + 1][y + 1] == 0 or board[x + 1][y + 1] * color_value < 0:
                    moves.append((x + 1, y + 1))
        
        if opp_capture_moves is not None:
            white_king_side_squares = [(7, 2), (7, 3), (7, 4)]
            white_queen_side_squares = [(7, 4), (7, 5), (7, 6)]
            black_king_side_squares = [(0, 2), (0, 3), (0, 4)]
            black_queen_side_squares = [(0, 4), (0, 5), (0, 6)]
            # Castling (white)
            if color_value == Player.white.value:

                # Queen side
                if castling_rights[Player.white]["queen_side"] and sum(board[7][1:4]) == 0 and not any(square in white_queen_side_squares for square in opp_capture_moves):
                    moves.append((7, 2))
                
                # King side
                if castling_rights[Player.white]["king_side"] and sum(board[7][5:7]) == 0 and not any(square in white_king_side_squares for square in opp_capture_moves):
                    moves.append((7, 6))
            
            # Castling (black)
            if color_value == Player.black.value:

                # King side
                if castling_rights[Player.black]["queen_side"] and sum(board[0][1:4]) == 0 and not any(square in black_queen_side_squares for square in opp_capture_moves):
                    moves.append((0, 2))
                
                # Queen side
                if castling_rights[Player.black]["king_side"] and sum(board[0][5:7]) == 0 and not any(square in black_king_side_squares for square in opp_capture_moves):
                    moves.append((0, 6))

        return moves
    
    @staticmethod
    def get_capture_moves(board, pos, possible_en_passant, color_value):
        return King.get_moves(board, pos, possible_en_passant, None, None, color_value)