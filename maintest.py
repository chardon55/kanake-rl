from pyce.chessboard import Chessboard


def main():
    cb = Chessboard()
    print(cb.numpy_chessboard)
    # cb.summary()
    cb2 = cb.copy()
    print(type(cb2))


if __name__ == '__main__':
    main()
    