from abc import abstractmethod

import chessboard as _cb


class Action:
    def __init__(self, chessboard: _cb.BaseChessboard) -> None:
        self._chessboard = chessboard

    @property
    def chessboard(self):
        return self._chessboard

    @abstractmethod
    def _locate_piece(self, action: int) -> tuple[2]:
        pass

    @abstractmethod
    def _read_action(self, action: int, source: tuple[2]) -> tuple[2]:
        pass

    def interpret(self, action: int) -> bool:
        pos = self._locate_piece(action)
        return self._chessboard.move_piece(pos, self._read_action(action, pos))
