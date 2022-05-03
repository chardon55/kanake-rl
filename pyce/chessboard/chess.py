import numpy as np

from pieces import pieces
from chessboard.chessboard import flip_chessboard, BaseChessboard
from rules import ChessRuleSet


RULE_SET = ChessRuleSet
RULE_SET_INSTANCE = None


def load_rule_set() -> RULE_SET:
    if not RULE_SET_INSTANCE:
        RULE_SET_INSTANCE = RULE_SET()

    return RULE_SET_INSTANCE


def init_chessboard():
    cb = np.zeros([8, 8], dtype=np.int8)

    for _ in range(2):
        cb[-2] = pieces["pawn"]
        cb[-1, 0] = cb[-1, -1] = pieces["rook"]
        cb[-1, 1] = cb[-1, -2] = pieces["knight"]
        cb[-1, 2] = cb[-1, -3] = pieces["bishop"]
        cb[-1, 3] = pieces["queen"]
        cb[-1, 4] = pieces["king"]

        cb = flip_chessboard(cb)

    return cb


class Chessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard())
        self.__rule_set = load_rule_set()

        # self._pieces = [
        #     [(6, i) for i in range(8)],
        #     [(7, 0), (7, 7)],
        #     [(7, 1), (7, 6)],
        #     [(7, 2), (7, 5)],
        #     [(7, 3)],
        #     [(7, 4)],
        # ]
        # self._pieces_c = [
        #     [(1, i) for i in range(8)],
        #     [(0, 0), (0, 7)],
        #     [(0, 1), (0, 6)],
        #     [(0, 2), (0, 5)],
        #     [(0, 3)],
        #     [(0, 4)],
        # ]

    def _check_rule(self, position, destination) -> bool:
        return self.__rule_set.check(self, position, destination)
