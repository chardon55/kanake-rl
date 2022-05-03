import numpy as np

from pieces import pieces_xq
from ruleset import RuleSet


class XiangqiRuleSet(RuleSet):
    __border = 5

    def _check_move(self, piece: int, chessboard: np.ndarray, source: tuple[2], delta: tuple[2], attacking: bool, target_piece: int) -> bool:
        s = False

        if piece == pieces_xq['soldier']:
            if source[0] < self.__border:
                s = abs(delta[0]) + abs(delta[1]) == 1 and delta[0] <= 0
            else:
                s = delta[0] == -1 and delta[1] == 0
        elif piece == pieces_xq['cannon']:
            s = not delta[0] * delta[1]

            if s and attacking:
                pass

        return s

    def _check_blocked(self, chessboard: np.ndarray, source: tuple[2], destination: tuple[2], delta: tuple[2]) -> bool:
        return super()._check_blocked(chessboard, source, destination, delta)

    def _check_promote(self, chessboard: np.ndarray, position: tuple[2], target_piece: int) -> bool:
        return super()._check_promote(chessboard, position, target_piece)
