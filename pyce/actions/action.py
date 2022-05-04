from abc import abstractmethod

from ..chessboard import BaseChessboard


class Action:
    def __init__(self, chessboard: BaseChessboard) -> None:
        self._chessboard = chessboard

    @property
    def chessboard(self):
        return self._chessboard

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

    def interpret(self, action: int) -> bool:
        piece, order = self._select_piece(action)
        pos = self._locate_piece(piece, order)
        return self._chessboard.move_piece(pos, self._read_action(action, pos))
