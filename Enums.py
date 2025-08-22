from enum import Enum

class HitterStats(Enum):
    TB = 0
    RBI = 1
    R = 2
    SB = 3
    BB = 4
    K = 5

class PitcherStats(Enum):
    IP = 0
    W = 1
    L = 2
    HD = 3
    SV = 4
    ER = 5
    H = 6
    K = 7
    BB = 8