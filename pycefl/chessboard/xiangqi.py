import numpy as np

from .chessboard import flip_chessboard, BaseChessboard
from ..pieces import pieces_xq


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


class XiangqiChessboard(BaseChessboard):
    def __init__(self) -> None:
        super().__init__(init_chessboard_xq())
