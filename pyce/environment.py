from pyce.chessboard import Chessboard, XiangqiChessboard, ShogiChessboard


TYPES = {
    "chess": 0,
    "xiangqi": 1,
    "shogi": 2,
}


CHESSBOARD = [
    Chessboard,
    XiangqiChessboard,
    ShogiChessboard,
]


class Environment:
    def __init__(self, _type: str) -> None:
        self._type = TYPES[_type]
        self._type_str = _type
        self.cb = CHESSBOARD[self._type]()

    @property
    def chessboard(self):
        return self.cb
