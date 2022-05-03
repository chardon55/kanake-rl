import numpy as np

from chessboard.chessboard import rotate_chessboard, BaseChessboard
from pieces import pieces_sg


def init_chessboard_sg():
    cb = np.zeros([9, 9], dtype=np.int8)

    for _ in range(2):
        cb[-3] = pieces_sg["fuhyou"]

        cb[-2, 1] = pieces_sg["kakugyou"]
        cb[-2, -2] = pieces_sg["hisha"]

        cb[-1, 0] = cb[-1, -1] = pieces_sg["kyousha"]
        cb[-1, 1] = cb[-1, -2] = pieces_sg["keima"]
        cb[-1, 2] = cb[-1, -3] = pieces_sg["ginshou"]
        cb[-1, 3] = cb[-1, -4] = pieces_sg["kinshou"]
        cb[-1, 4] = pieces_sg["oushou"]

        cb = rotate_chessboard(cb)

    return cb


class ShogiChessboard(BaseChessboard):
    def __init__(self, is_defender=False) -> None:
        super().__init__(init_chessboard_sg())
        self.__defend = is_defender

    def switch_player(self):
        self.cb = rotate_chessboard(self.cb)
        self.__defend = not self.__defend

    @property
    def is_defender(self):
        return self.__defend
