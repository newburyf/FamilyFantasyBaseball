from enum import Enum

class HitterStats(Enum):
    TB = 0
    RBI = 1
    R = 2
    SB = 3
    BB = 4
    K = 5

#              [tb, rbi, r, sb, bb, k]
HitterPoints = [1, 1, 1, 1, 1, -1]

class PitcherStats(Enum):
    O = 0
    W = 1
    L = 2
    HD = 3
    SV = 4
    ER = 5
    H = 6
    K = 7
    BB = 8

#               [o, w, l, hd, sv, er, h, k, bb]
PitcherPoints = [1, 2, -2, 2, 5, -2, -1, 1, -1]