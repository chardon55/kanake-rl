from pycefl.chessboard import Chessboard
from pycefl.actions import ChessAction


def main():
    cb = Chessboard()
    action_set = ChessAction(cb)

    cb.cb[7, -2] = cb.cb[7, -3] = 0

    action_set.perform(13)
    action_set.perform(161)
    # action_set.perform(162)
    # action_set.perform(93)
    action_set.perform(202)
    action_set.perform(225)
    # cb.switch_player()
    print(cb)


if __name__ == '__main__':
    main()
    