from ..chessboard import BaseChessboard
from ..actions import ActionSet
from ..reward_function import RewardFunction
from ..ceil import CEIL


ceil_interpreter = CEIL()


class Environment:
    def __init__(self, chessboard: BaseChessboard) -> None:
        self.__cb = chessboard
        self.__ceil = ceil_interpreter

    @property
    def chessboard(self):
        return self.__cb

    @property
    def interpreter(self):
        return self.__ceil

    def step(self, action: int):
        pass


# class CommonEnvironment:
#     def __init__(self, _type: str) -> None:
#         self._type = TYPES[_type]
#         self._type_str = _type
#         self.cb = CHESSBOARD[self._type]()

#     @property
#     def chessboard(self):
#         return self.cb
