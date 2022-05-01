from abc import abstractmethod
from typing import overload
import warnings
import numpy as np

from pieces import pieces, pieces_sg, pieces_xq


def flip_chessboard(cb: np.ndarray):
    return -cb[::-1]


def rotate_chessboard(cb: np.ndarray):
    return -cb[::-1, ::-1]


class BaseChessboard:
    def __init__(self, cb: np.ndarray) -> None:
        self.cb = cb

    @abstractmethod
    def _check_rule(self, position, destination) -> bool:
        pass

    def move_piece(self, position, destination) -> bool:
        if not self._check_rule(position, destination):
            return False

        self.cb[destination[0], destination[1]] \
            = self.cb[position[0], position[1]]
        self.cb[position[0], position[1]] = 0
        return True

    def switch_player(self):
        self.cb = flip_chessboard(self.cb)

    @property
    def numpy_chessboard(self):
        return self.cb


class Chessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard())


class XiangqiChessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard_xq())


class ShogiChessboard(BaseChessboard):
    def __init__(self, is_defender=False) -> None:
        super().__init__(init_chessboard_sg())
        self.__defend = is_defender

    @overload
    def switch_player(self):
        self.cb = rotate_chessboard(self.cb)
        self.__defend = not self.__defend

    @property
    def is_defender(self):
        return self.__defend


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


def init_chessboard_xq():
    cb = np.zeros([10, 9], dtype=np.int8)

    for _ in range(2):
        for i in range(5):
            cb[-4, i * 2] = pieces_xq["soldier"]

        cb[-3, 1] = cb[-3, -2] = pieces_xq["cannon"]
        cb[-1, 0] = cb[-1, -1] = pieces_xq["chariot"]
        cb[-1, 1] = cb[-1, -2] = pieces_xq["horse"]
        cb[-1, 2] = cb[-1, -3] = pieces_xq["elephant"]
        cb[-1, 3] = cb[-1, -4] = pieces_xq["mandarin"]
        cb[-1, 4] = pieces_xq["general"]

        cb = flip_chessboard(cb)

    return cb


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


def main():
    print(init_chessboard_sg())


if __name__ == '__main__':
    main()
