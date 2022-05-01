from abc import abstractmethod
import numpy as np

import chessboard as _cb


class Action:
    def __init__(self, chessboard: _cb.BaseChessboard) -> None:
        self._chessboard = chessboard

    @property
    def chessboard(self):
        return self._chessboard

    @abstractmethod
    def _check_piece(self, action: int) -> int:
        pass

    @abstractmethod
    def _locate_piece(self, target_piece: int) -> tuple[2]:
        pass

    def interpret(self, action: int):
        cb = self._chessboard.numpy_chessboard
        r, c = cb.shape
        tp = self._check_piece(action)

        pos = self._locate_piece(tp)
        # TODO
