from abc import abstractmethod

from ..chessboard import BaseChessboard


class ActionSet:
    def __init__(self, chessboard: BaseChessboard) -> None:
        self.__chessboard = chessboard

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

    def interpret(self, action: int) -> tuple[2]:
        piece, order = self._select_piece(action)
        pos = self._locate_piece(piece, order)
        return pos, self._read_action(action, pos)

    def perform(self, action: int) -> bool:
        return self.__chessboard.move_piece(*self.interpret(action))

    def simulate(self):
        pass


class ActionSimulator:
    def __init__(self, action_set: ActionSet) -> None:
        self.__action_set = action_set
        # TODO

    def __call__(self, action: int) -> bool:
        return self.forward(action)

    def forward(self, action: int) -> bool:
        pass
        # self.__action_set.
        # self.__action_set.chessboard._check_rule()

    def reverse(self):
        pass
