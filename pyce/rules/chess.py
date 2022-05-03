import numpy as np

import pieces as ps
from ruleset import RuleSet


class ChessRuleSet(RuleSet):
    def _check_move(self, piece: int, chessboard: np.ndarray, source: tuple[2], delta: tuple[2], attacking: bool, target_piece: int) -> bool:
        s = False

        if piece == ps.pieces['pawn']:
            if delta[0] < 0:
                if attacking:
                    s = (delta[1] == 1 or delta[1] == -1) and delta[0] == -1
                else:
                    s = not delta[1] \
                        and (delta[0] == -1 or (delta[0] == -2 if source[0] == 6 else False))
        elif piece == ps.pieces['rook']:
            s = not delta[0] * delta[1]
        elif piece == ps.pieces['knight']:
            s = abs(delta[0] * delta[1]) == 2
        elif piece == ps.pieces['bishop']:
            s = abs(delta[0]) == abs(delta[1])
        elif piece == ps.pieces['queen']:
            s = not delta[0] * delta[1] or abs(delta[0]) == abs(delta[1])
        elif piece == ps.pieces['king']:
            s = abs(delta[0]) <= 1 and abs(delta[1]) <= 1

        return s

    def _check_blocked(self, chessboard: np.ndarray, source: tuple[2], destination: tuple[2], delta: tuple[2]) -> bool:
        p = chessboard[source[0], source[1]]
        # if p == ps.pieces['knight']:
        #     return False

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
            and chessboard[position[0], position[1]] == ps.pieces['pawn'] \
            and target_piece != ps.pieces['pawn'] \
            and target_piece != ps.pieces['king']
