from abc import abstractmethod
from defusedxml import NotSupportedError
import numpy as np
from pycefl.chessboard import BaseChessboard


class BaseChessRenderer:
    @abstractmethod
    def _render(self, cb: np.ndarray):
        pass

    def render(self, chessboard):
        if isinstance(chessboard, BaseChessboard):
            chessboard = chessboard.numpy_chessboard
        elif not isinstance(chessboard, np.ndarray):
            raise NotSupportedError()

        self._render(chessboard)
