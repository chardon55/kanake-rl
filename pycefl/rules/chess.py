import numpy as np

from ..pieces import pieces
from .ruleset import RuleSet


class ChessRuleSet(RuleSet):
    def _check_move(self, piece: int, chessboard: np.ndarray, source: tuple[2], delta: tuple[2], attacking: bool, target_piece: int, challenger: bool) -> bool:
        s = False

        if piece == pieces['pawn']:
            if delta[0] < 0:
                if attacking:
                    s = (delta[1] == 1 or delta[1] == -1) and delta[0] == -1
                else:
                    s = not delta[1] \
                        and (delta[0] == -1 or (delta[0] == -2 if source[0] == 6 else False))
        elif piece == pieces['rook']:
            s = not delta[0] * delta[1]
        elif piece == pieces['knight']:
            s = abs(delta[0] * delta[1]) == 2
        elif piece == pieces['bishop']:
            s = abs(delta[0]) == abs(delta[1])
        elif piece == pieces['queen']:
            s = not delta[0] * delta[1] or abs(delta[0]) == abs(delta[1])
        elif piece == pieces['king']:
            s = abs(delta[0]) <= 1 and abs(delta[1]) <= 1
            if not s and not delta[0] and abs(delta[1]) == 2 and source == (7, (3 if challenger else 4)):
                if delta[1] > 0:
                    s = chessboard[7, 7] == pieces['rook'] \
                        and not chessboard[7, 6]\
                        and not chessboard[7, 5]

                else:
                    s = chessboard[7, 0] == pieces['rook'] \
                        and not chessboard[7, 1]\
                        and not chessboard[7, 2]

        return s

    def _check_blocked(self, chessboard: np.ndarray, source: tuple[2], destination: tuple[2], delta: tuple[2]) -> bool:
        p = chessboard[source[0], source[1]]
        # if p == ps.pieces['knight']:
        #     return False

        if chessboard[destination[0], destination[1]] > 0:
            return True

        s = False

        sgns = np.sign(delta)
        if not delta[0] * delta[1]:
            if delta[0]:
                for i in range(source[0] + sgns[0], destination[0] + sgns[0], sgns[0]):
                    target_p = chessboard[i, destination[1]]
                    s = target_p > 0 if i == destination[0] else target_p != 0
                    if s:
                        break
            else:
                for i in range(source[1] + sgns[1], destination[1] + sgns[1], sgns[1]):
                    target_p = chessboard[destination[0], i]
                    s = target_p > 0 if i == destination[1] else target_p != 0
                    if s:
                        break

        elif abs(delta[0]) == abs(delta[1]):
            for i in range(1, abs(delta[0]) + 1):
                pos = (source[0] + i * sgns[0], source[1] + i * sgns[1])
                target_p = chessboard[pos[0], pos[1]]
                s = target_p > 0 if pos == destination else target_p != 0
                if s:
                    break

        return s

    def _check_promote(self, chessboard: np.ndarray, position: tuple[2], target_piece: int) -> bool:
        return not position[0] \
            and chessboard[position[0], position[1]] == pieces['pawn'] \
            and target_piece != pieces['pawn'] \
            and target_piece != pieces['king']
