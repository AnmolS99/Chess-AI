from enum import Enum
from numba import int8

class Player(Enum):
    white = 1
    black = -1

Player = int8