from abc import abstractmethod
import numpy as np


def flip_chessboard(cb: np.ndarray):
    return -cb[::-1]


def rotate_chessboard(cb: np.ndarray):
    return -cb[::-1, ::-1]


class BaseChessboard:
    def __init__(self, cb: np.ndarray) -> None:
        self.cb = cb
        # self._pieces = []
        # self._pieces_c = []

    @abstractmethod
    def _check_rule(self, position, destination) -> bool:
        pass

    def __move(self, source: tuple[2], destination: tuple[2]):
        # p = self.cb[source[0], source[1]]

        self.cb[destination[0], destination[1]] \
            = self.cb[source[0], source[1]]
        self.cb[source[0], source[1]] = 0

        # if p > 0:
        #     for i, pos in enumerate(self._pieces[p]):
        #         if source == pos:
        #             self._pieces[p][i] = [*source]
        #             break

        # tp = self.cb[destination[0], destination[1]]
        # if tp > 0:
        #     for i, pos in enumerate(self._pieces[tp]):
        #         if destination == pos:
        #             del self._pieces[tp][i]
        #             break

    def move_piece(self, position, destination) -> bool:
        if not self._check_rule(position, destination):
            return False

        self.__move(position, destination)
        return True

    def switch_player(self):
        self.cb = flip_chessboard(self.cb)

    def transit(self, source: tuple[2], destination: tuple[2]):
        if self.cb[source[0], source[1]] >= 0:
            return

        self.__move(source, destination)

    @property
    def numpy_chessboard(self):
        return self.cb
