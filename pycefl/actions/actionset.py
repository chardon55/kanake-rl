from abc import abstractmethod
from collections import namedtuple
import numpy as np

from pycefl.exceptions.actionset import PieceNotFoundError

from ..chessboard import BaseChessboard

PerformanceInfo = namedtuple('MDPInfo', (
    'reward',
    'done',
    'success',
))


class ActionSet:
    def __init__(self, chessboard: BaseChessboard) -> None:
        self.__chessboard = chessboard
        self.__shape = self.chessboard.numpy_chessboard.shape

    def action_number(self):
        pass

    @property
    def chessboard(self):
        return self.__chessboard

    @abstractmethod
    def _select_piece(self, action: int) -> tuple[2]:
        """
            :returns
                A tuple containing the piece's class and a 1-based index to
                determine which of the pieces in this class should be selected
        """
        pass

    @abstractmethod
    def _locate_piece(self, piece: int, order: int) -> tuple[2]:
        pass

    @abstractmethod
    def _read_action(self, action: int, source: tuple[2]) -> tuple[2]:
        pass

    def __call__(self, action: int) -> bool:
        return self.perform(action)

    def interpret(self, action: int) -> tuple[4]:
        piece, order = self._select_piece(action)
        pos = self._locate_piece(piece, order)
        dest = self._read_action(action, pos)

        dest = min(self.__shape[0] - 1, dest[0]
                   ), min(self.__shape[1] - 1, dest[1])

        return piece, self.chessboard.numpy_chessboard[dest[0], dest[1]], pos, dest

    def perform(self, action: int) -> PerformanceInfo:
        try:
            piece, target_piece, src, dest = self.interpret(action)
        except PieceNotFoundError:
            return PerformanceInfo(0, False, False)

        success = self.__chessboard.move_piece(src, dest)
        reward = self._calculate_reward(
            self.__chessboard, piece, target_piece, src, dest, success
        )
        done = self._assume_end(
            self.__chessboard, piece, target_piece, src, dest
        )

        return PerformanceInfo(reward, done, success)

    def simulate(self):
        return ActionSimulator(self)

    @abstractmethod
    def _calculate_reward(self, chessboard: BaseChessboard, piece: int, target_piece: int, source: tuple[2], destination: tuple[2], success: bool) -> float:
        return 0

    @abstractmethod
    def _assume_end(self, chessboard: BaseChessboard, piece: int, target_piece: int, source: tuple[2], destination: tuple[2]) -> bool:
        return False


class ActionSimulator:
    def __init__(self, action_set: ActionSet) -> None:
        self.__action_set = action_set
        self.__moves = []
        self.__cb = None
        self.__update_state()

    def __call__(self, action: int) -> bool:
        return self.forward(action)

    def __get_final(self):
        return self.__moves[0][0], self.__moves[-1][-1]

    def __copy_chessboard(self):
        return self.__action_set.chessboard.cb.copy()

    def __update_state(self):
        self.__cb = self.__copy_chessboard()
        self.__moves.clear()

    def __move(self, source: tuple[2], destination: tuple[2]):
        self.cb[destination[0], destination[1]] \
            = self.cb[source[0], source[1]]
        self.cb[source[0], source[1]] = 0

    def forward(self, action: int) -> bool:
        try:
            src, dest = self.__action_set.interpret(action)
        except PieceNotFoundError:
            return False

        if len(self.__moves) > 0 and src != self.__moves[-1][-1]:
            return False

        self.__moves.append((src, dest))
        self.__move(src, dest)

        s = self.__action_set\
                .__chessboard\
                ._check_rule(*self.__get_final())

        if not s:
            self.reverse()

        return s

    def reverse(self):
        src, dest = self.__moves.pop()
        self.__move(dest, src)

    def reset(self):
        self.__update_state()

    @property
    def final_action(self):
        return self.__get_final()

    def perform(self) -> bool:
        if not len(self.__moves):
            return False

        s = self.__action_set\
                .chessboard\
                .move_piece(*self.__get_final())
        if s:
            self.__update_state()

        return s

    @property
    def current_state(self) -> np.ndarray:
        return self.__cb
