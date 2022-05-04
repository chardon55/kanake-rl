from .action import Action


RANGES = (0, 23, 31, 47, 55, 63, 71, 73)


class ChessAction(Action):
    def _select_piece(self, action: int) -> tuple[2]:
        piece, c = 0, 0
        # TODO
