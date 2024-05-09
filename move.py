from fen_converter import FENConverter

class Move:

    def __init__(self, start_pos, end_pos, end_piece, promotion=False) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.end_piece = end_piece
        self.promotion = promotion

    def __eq__(self, other_move):
        if isinstance(other_move, Move):
            return (self.start_pos == other_move.start_pos and 
                    self.end_pos == other_move.end_pos and 
                    self.end_piece == other_move.end_piece)
        return False
    
    def __str__(self):
        return f"{FENConverter.pos_to_notation(self.start_pos)}{FENConverter.pos_to_notation(self.end_pos)}{FENConverter.piece_to_fen_char(self.end_piece) if self.promotion else ''}"