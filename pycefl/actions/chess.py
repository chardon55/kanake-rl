import math
from .actionset import ActionSet
from ..chessboard import Chessboard
from ..pieces import pieces_count, pieces_names, pieces
from ..exceptions import InvalidTypeError, PieceNotFoundError


RANGES_CLASSIC = (0, 32, 88, 104, 160, 216, 224, 226)
RANGES_REDUCED = (0, 24, 32, 48, 56, 64, 72, 74)


class ChessActionSet(ActionSet):
    def __init__(self, chessboard: Chessboard, type: str = "classic") -> None:
        super().__init__(chessboard)
        self.__type = type

    def _select_piece(self, action: int) -> tuple[2]:
        piece, c = 0, 0

        if self.__type == 'classic':
            ch_range = RANGES_CLASSIC
        elif self.__type == 'reduced':
            ch_range = RANGES_REDUCED
        else:
            raise InvalidTypeError()

        if action in range(ch_range[-2], ch_range[-1]):
            piece = pieces['king']
            c = 0
        else:
            for i, pc in enumerate(pieces_count[1:], start=1):
                if action in range(ch_range[i-1], ch_range[i]):
                    piece = i
                    c = math.floor((action - ch_range[i-1]
                                    ) / ((ch_range[i] - ch_range[i-1]) / pc))
                    break

        return piece, c

    def _locate_piece(self, piece: int, order: int) -> tuple[2]:
        cb = self.chessboard.numpy_chessboard
        r, c = cb.shape

        cur_order = 0
        for j in range(c):
            for i in range(r):
                if cb[i, j] == piece:
                    if cur_order >= order:
                        return i, j
                    cur_order += 1

        raise PieceNotFoundError()

    def _read_action(self, action: int, source: tuple[2]) -> tuple[2]:
        delta = [0, 0]

        if self.__type == 'classic':
            ch_range = RANGES_CLASSIC
        elif self.__type == 'reduced':
            ch_range = RANGES_REDUCED
        else:
            raise InvalidTypeError()

        if action in range(ch_range[-2], ch_range[-1]):
            delta[1] = 2 * (-1 if action == ch_range[-2] else 1)
        else:
            for i, pc in enumerate(pieces_count[1:], start=1):
                if action in range(ch_range[i-1], ch_range[i]):
                    t = (action - ch_range[i-1]
                         ) % ((ch_range[i] - ch_range[i-1]) / pc)
                    if i == pieces['knight']:
                        delta[0] = (t % 2 + 1)
                        delta[1] = 3 - delta[0]

                        if t in (2, 3, 4, 5):
                            delta[0] = -delta[0]

                        if t in (2, 3, 6, 7):
                            delta[1] = -delta[1]
                    elif i == pieces['king']:
                        if t in (0, 4, 7):
                            delta[1] = 1
                        elif t in (2, 5, 6):
                            delta[1] = -1

                        if t in (1, 4, 5):
                            delta[0] = 1
                        elif t in (3, 6, 7):
                            delta[0] = -1
                    else:
                        if self.__type == 'classic':
                            if i == pieces['pawn']:
                                delta[0] = (-2 if t == 1 else -1)
                                if t == 2:
                                    delta[1] = -1
                                elif t == 3:
                                    delta[1] = 1

                            elif i == pieces['rook']:
                                distance = t % 7
                                direction = int(t / 7)
                                if direction == 0:
                                    delta[1] = distance
                                elif direction == 1:
                                    delta[0] = -distance
                                elif direction == 2:
                                    delta[1] = -distance
                                else:
                                    delta[0] = distance
                            elif i == pieces['bishop']:
                                distance = t % 7 + 1
                                direction = int(t / 7) + 1
                                delta[0] = delta[1] = distance
                                if direction in (2, 3):
                                    delta[0] = -delta[0]

                                if direction in (1, 2):
                                    delta[1] = -delta[1]
                            elif i == pieces['queen']:
                                delimiter = (ch_range[i] - ch_range[i-1]) // 2
                                group = t // delimiter
                                t %= delimiter

                                distance = t % 7 + 1
                                direction = int(t / 7) + 1
                                if group:
                                    delta[0] = delta[1] = distance
                                    if direction in (2, 3):
                                        delta[0] = -delta[0]

                                    if direction in (1, 2):
                                        delta[1] = -delta[1]
                                else:
                                    if direction == 0:
                                        delta[1] = distance
                                    elif direction == 1:
                                        delta[0] = -distance
                                    elif direction == 2:
                                        delta[1] = -distance
                                    else:
                                        delta[0] = distance

                        elif self.__type == 'reduced':
                            if i == pieces['pawn']:
                                delta[0] = -1
                                if t == 1:
                                    delta[1] = -1
                                elif t == 2:
                                    delta[1] = 1
                            elif i == pieces['rook']:
                                if t == 1:
                                    delta[0] = 1
                                elif t == 3:
                                    delta[0] = -1

                                if t == 0:
                                    delta[1] = 1
                                elif t == 2:
                                    delta[1] = -1
                            elif i == pieces['bishop']:
                                delta[0] = delta[1] = 1
                                if t in (1, 2):
                                    delta[0] = -delta[0]

                                if t in (2, 3):
                                    delta[1] = -delta[1]
                            elif i == pieces['queen']:
                                group = int(t / 2)
                                t %= 2

                                if group:
                                    delta[0] = delta[1] = 1
                                    if t in (1, 2):
                                        delta[0] = -delta[0]

                                    if t in (2, 3):
                                        delta[1] = -delta[1]
                                else:
                                    if t == 1:
                                        delta[0] = 1
                                    elif t == 3:
                                        delta[0] = -1

                                    if t == 0:
                                        delta[1] = 1
                                    elif t == 2:
                                        delta[1] = -1

                        else:
                            raise InvalidTypeError()
                        break

        return int(source[0] + delta[0]), int(source[1] + delta[1])

    def _calculate_reward(self, chessboard: Chessboard, piece: int, target_piece: int, source: tuple[2], destination: tuple[2]) -> float:
        if target_piece == -pieces['king']:
            return 150.

        if target_piece == -pieces['queen']:
            return 30. + 8. * destination[0]

        if target_piece == -pieces['pawn']:
            return 1. + (destination[0] - 1.) ** 3. / 3.

        if target_piece in (-pieces['rook'], -pieces['bishop']):
            return 10. + 7. * destination[0]

        if target_piece == -pieces['knight']:
            return 5. + 5. * destination[0]

        return -.05

    def _assume_end(self, chessboard: Chessboard, piece: int, target_piece: int, source: tuple[2], destination: tuple[2]) -> bool:
        return abs(target_piece) == pieces['king']
