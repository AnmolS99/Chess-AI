from pieces.piece import Piece


class King(Piece):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_moves(board, pos, color):
        moves = []
        x, y = pos
        if x > 0:
            # Up
            if board[x - 1][y] == 0 or board[x - 1][y] * color.value < 0:
                moves.append((x - 1, y))
            
            # Up-left
            if y > 0:
                if board[x - 1][y - 1] == 0 or board[x - 1][y - 1] * color.value < 0:
                    moves.append((x - 1, y - 1))
            
            # Up-right
            if y < 7:
                if board[x - 1][y + 1] == 0 or board[x - 1][y + 1] * color.value < 0:
                    moves.append((x - 1, y + 1))
        
        if y > 0:

            # Left
            if board[x][y - 1] == 0 or board[x][y - 1] * color.value < 0:
                    moves.append((x, y - 1))
        
        if y < 7:

            # Right
            if board[x][y + 1] == 0 or board[x][y + 1] * color.value < 0:
                    moves.append((x, y + 1))

        if x < 7:
            # Down
            if board[x + 1][y] == 0 or board[x + 1][y] * color.value < 0:
                moves.append((x + 1, y))
            
            # Down-left
            if y > 0:
                if board[x + 1][y - 1] == 0 or board[x + 1][y - 1] * color.value < 0:
                    moves.append((x + 1, y - 1))
            
            # Dwon-right
            if y < 7:
                if board[x + 1][y + 1] == 0 or board[x + 1][y + 1] * color.value < 0:
                    moves.append((x + 1, y + 1))
        
        return moves