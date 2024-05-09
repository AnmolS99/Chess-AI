"""Class converting to and from Forsyth-Edwards Notation"""
import numpy as np
from player import Player


piece_values = {'P': 1, 'N': 3, 'B': 4, 'R': 2, 'Q': 5, 'K': 6, 'p': -1, 'n': -3, 'b': -4, 'r': -2, 'q': -5, 'k': -6}

class FENConverter:

    def __init__(self) -> None:
        pass

    def to_game_state(self, board, fen_string: str):
        fen_fields = fen_string.split(" ")
        
        # Setting board state
        fen_board = np.zeros((8, 8))
        board_rows = fen_fields[0].split("/")
        rank = 0
        for board_row in board_rows:
            col_no = 0
            for char in board_row:
                if char.isdigit():
                    fen_board[rank][col_no:col_no+int(char)] = 0
                    col_no += int(char)
                else:
                    piece_value = piece_values[char]
                    if piece_value == 6:
                        board.king_position[Player.white] = (rank, col_no)
                    elif piece_value == -6:
                        board.king_position[Player.black] = (rank, col_no)
                    fen_board[rank][col_no] = piece_value
                    col_no += 1
            rank += 1
        board.board = fen_board

        board.turn = Player.white if fen_fields[1] == 'w' else Player.black


        board.castling_rights[Player.white]["king_side"] = True if 'K' in fen_fields[2] else False
        board.castling_rights[Player.white]["queen_side"] = True if 'Q' in fen_fields[2] else False
        board.castling_rights[Player.black]["king_side"] = True if 'k' in fen_fields[2] else False
        board.castling_rights[Player.black]["queen_side"] = True if 'q' in fen_fields[2] else False
        
        if fen_fields[3] == '-':
            pass
        else:
            board.possible_en_passant = self.get_possible_en_passant(fen_fields[3])
        
    
    def get_possible_en_passant(self, skipped_square: str):
        row, col = self.notation_to_pos(skipped_square)
        if row == 5:
            row -= 1
        elif row == 2:
            row += 1
        else:
            Exception("FEN provided en passant square has to be on rank 3 or 6")
        return (row, col)


    def notation_to_pos(self, notation_pos: str):
        row = 8 - int(notation_pos[1])
        col = 97 - ord(notation_pos[0])
        return (row, col)
    
    @staticmethod
    def pos_to_notation(pos):
        row, col = pos
        row = 8 - row
        col = chr(97 + col)
        return col + str(row)
    
    def piece_to_fen_char(piece_value: int):
        for k, v in piece_values.items():
            if v == piece_value:
                return k.lower()
        return None

