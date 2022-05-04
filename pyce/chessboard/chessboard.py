from abc import abstractmethod
import numpy as np


SEP = "-" * 20


def flip_chessboard(cb: np.ndarray):
    return -cb[::-1]


def rotate_chessboard(cb: np.ndarray):
    return -cb[::-1, ::-1]


class BaseChessboard:
    def __init__(self, cb: np.ndarray) -> None:
        self.cb = cb
        self._piece_names = None
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

    def summary(self):
        arr = np.array([0 for _ in range(len(self._piece_names) * 2 - 1)])

        for x in np.nditer(self.cb):
            arr[x] += 1

        print(SEP)
        print("Summary")
        print(SEP)

        print(self.cb)
        print(SEP)

        print('Self')
        for i, name in enumerate(self._piece_names[1:]):
            print(f"{name}:\t{arr[i+1]}")
        print()

        print('Competitor')
        for i, name in enumerate(self._piece_names[1:]):
            print(f"{name}:\t{arr[-i-1]}")

        print()
        print(f"Empty:\t{arr[0]}")
        print(SEP)
