from abc import abstractmethod
from defusedxml import NotSupportedError
import numpy as np
from pyce.chessboard import BaseChessboard


class BaseChessRenderer:
    @abstractmethod
    def _render(self, cb: np.ndarray):
        pass

    def render(self, chessboard):
        if isinstance(chessboard, BaseChessboard):
            chessboard = chessboard.to_numpy()
        elif not isinstance(chessboard, np.ndarray):
            raise NotSupportedError()

        self._render(chessboard)
