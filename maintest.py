from pyce.chessboard import Chessboard


def main():
    cb = Chessboard()
    print(cb.numpy_chessboard)
    cb.summary()


if __name__ == '__main__':
    main()
    