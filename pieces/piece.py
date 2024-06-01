from player import Player


class Piece:

    def __init__(self):
        pass

    def get_moves(self, board, pos, possible_en_passant, castling_rights, opp_capture_moves, color_value):
        pass

    def get_capture_moves(self, board, pos, color_value):
        """
        Get all moves that attacks a king (en passant is not included)
        """
        pass