from abc import abstractmethod
import numpy as np

from ..chessboard import BaseChessboard


class RuleSet:
    @abstractmethod
    def _check_move(self, piece: int, chessboard: np.ndarray, source: tuple[2], delta: tuple[2], attacking: bool, target_piece: int) -> bool:
        pass

    @abstractmethod
    def _check_blocked(self, chessboard: np.ndarray, source: tuple[2], destination: tuple[2], delta: tuple[2]) -> bool:
        pass

    def check(self, chessboard: BaseChessboard, source: tuple[2], destination: tuple[2]) -> bool:
        cb = chessboard.numpy_chessboard
        r, c = cb.shape
        d0, d1 = destination
        s0, s1 = source

        if s0 < 0 or s1 < 0 or s0 >= r or s1 >= c:
            return False

        # Return false if the piece does not exist or belongs to the competitor
        if cb[s0, s1] <= 0:
            return False

        if source == destination:
            return True

        if d0 < 0 or d1 < 0 or d0 >= r or d1 >= c:
            return False

        target_p = cb[d0, d1]
        delta = d0 - s0, d1 - s1
        return self._check_move(cb[s0, s1], cb, source, delta, target_p < 0, target_p) \
            and not self._check_blocked(cb, source, destination, delta)

    @abstractmethod
    def _check_promote(self, chessboard: np.ndarray, position: tuple[2], target_piece: int) -> bool:
        pass

    def promote_piece(self, chessboard: BaseChessboard, position: tuple[2], target_piece: int, check_only=False) -> bool:
        cb = chessboard.numpy_chessboard

        shape = cb.shape
        p0, p1 = position
        if p0 >= shape[0] or p1 >= shape[1] or p0 < 0 or p1 < 0:
            return False

        s = self._check_promote(cb, position, target_piece)
        if s and not check_only:
            cb[position[0], position[1]] = target_piece

        return s
