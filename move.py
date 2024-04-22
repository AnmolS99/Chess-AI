class Move:

    def __init__(self, start_pos, end_pos, end_piece) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.end_piece = end_piece

    def __eq__(self, other_move):
        if isinstance(other_move, Move):
            return (self.start_pos == other_move.start_pos and 
                    self.end_pos == other_move.end_pos and 
                    self.end_piece == other_move.end_piece)
        return False