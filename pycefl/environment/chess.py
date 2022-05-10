from .environment import Environment
from ..chessboard import Chessboard
from ..actions import ChessActionSet


class ChessEnvironment(Environment):
    def __init__(self, _type='classic') -> None:
        super().__init__(ChessActionSet)

    def _init_chessboard(self):
        return Chessboard()
