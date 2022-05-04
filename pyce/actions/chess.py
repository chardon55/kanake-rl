from .actionset import ActionSet


RANGES = (0, 23, 31, 47, 55, 63, 71, 73)


class ChessAction(ActionSet):
    def _select_piece(self, action: int) -> tuple[2]:
        piece, c = 0, 0
        # TODO
