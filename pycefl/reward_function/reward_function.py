from ..chessboard import BaseChessboard


class RewardFunction:
    def __init__(self, chessboard: BaseChessboard) -> None:
        self.__cb = chessboard

    @property
    def chessboard(self):
        return self.__cb

    def calculate(self, piece: int, target_piece: int, source: tuple[2], destination: tuple[2]) -> float:
        pass
