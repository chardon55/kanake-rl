from abc import abstractmethod
import numpy as np

import pyce.chessboard as _cb


class RuleSet:
    @abstractmethod
    def _check_move(self, chessboard: np.ndarray, source: tuple[2], destination: tuple[2]) -> bool:
        pass

    def check(self, chessboard: _cb.BaseChessboard, source: tuple[2], destination: tuple[2]) -> bool:
        cb = chessboard.to_numpy()
        r, c = cb.shape
        d0, d1 = destination[0], destination[1]
        s0, s1 = source[0], source[1]

        if s0 < 0 or s1 < 0 or s0 >= r or s1 >= c:
            return False

        # Return false if the piece does not exist or belongs to the competitor
        if cb[s0, s1] <= 0:
            return False

        if d0 < 0 or d1 < 0 or d0 >= r or d1 >= c:
            return False

        return self._check_move(cb, source, destination)
