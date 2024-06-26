from enum import Enum

class Player(Enum):
    white = 1
    black = -1

class PlayerType(Enum):
    User = "User",
    Random = "Random"
    MiniMax = "MiniMax"
    AlphaBeta = "AlphaBeta"
    AlphaBetaV2 = "AlphaBetaV2"
    MCTS = "MCTS"