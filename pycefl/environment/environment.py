from abc import abstractmethod
from collections import namedtuple
from typing import Type
import numpy as np
from ..chessboard import BaseChessboard
from ..actions import ActionSet
from ..ceil import CEIL


ceil_interpreter = CEIL()

MDPInfo = namedtuple('MDPInfo', (
    'state',
    'state2',
    'reward',
    'done',
    'success',
))


class Environment:
    def __init__(self, action_set_type: Type[ActionSet]) -> None:
        self.__cb: BaseChessboard = None
        self.__ceil = ceil_interpreter
        self.__action_set = None
        self.__action_set_type = action_set_type

    @property
    def action_set(self):
        return self.__action_set

    @property
    def chessboard(self):
        return self.__cb

    @property
    def interpreter(self):
        return self.__ceil

    @abstractmethod
    def _init_chessboard(self):
        pass

    def reset(self):
        self.__cb = self._init_chessboard()
        self.__action_set = self.__action_set_type(self.__cb)
        return self

    def shift(self):
        self.__cb.switch_player(flip=False)

    def flip(self):
        self.__cb.switch_player(flip=True)

    def step(self, action: int) -> MDPInfo:
        state = self.__cb.numpy_chessboard.copy()
        reward, done, success = self.__action_set.perform(action)
        state2 = self.__cb.numpy_chessboard.copy() if not done else None

        return MDPInfo(state, state2, reward, done, success)

    def update_state(self, state: np.ndarray):
        if state.shape == self.__cb.numpy_chessboard.shape:
            self.__cb.cb = state.copy()


# class CommonEnvironment:
#     def __init__(self, _type: str) -> None:
#         self._type = TYPES[_type]
#         self._type_str = _type
#         self.cb = CHESSBOARD[self._type]()

#     @property
#     def chessboard(self):
#         return self.cb
