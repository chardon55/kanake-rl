from abc import abstractmethod
from turtle import pos
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

        value = self.cb[position[0], position[1]]
        self.cb[destination[0], destination[1]] = value
        self.cb[position[0], position[1]] = 0
        return True


class Chessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard())


class XiangqiChessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard_xq())


class ShogiChessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard_sg())


def init_chessboard():
    cb = np.zeros([8, 8])

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
    cb = np.zeros([10, 9])

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
    cb = np.zeros([9, 9])

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
