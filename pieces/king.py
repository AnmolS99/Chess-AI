from pieces.piece import Piece


class King(Piece):

    def __init__(self, color: int, x: int, y: int):
        super().__init__(color, x, y, "king")