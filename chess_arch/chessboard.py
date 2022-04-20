import numpy as np


pieces = {
    "pawn": 1,      # 🨅
    "rook": 2,      # 🨂
    "knight": 3,    # 🨄
    "bishop": 4,    # 🨃
    "queen": 5,     # 🨁
    "king": 6,      # 🨀
}

pieces_xq = {
    "soldier": 1,   # 🩦 🩭
    "cannon": 2,    # 🩥 🩬
    "chariot": 3,   # 🩤 🩫
    "horse": 4,     # 🩣 🩪
    "elephant": 5,  # 🩢 🩩
    "mandarin": 6,  # 🩡 🩨
    "general": 7,   # 🩠 🩧
}

pieces_sg = {
    "fuhyou": 1,        # 歩兵 P
    "tokin": 2,         # と金 +P
    "kyousha": 3,       # 香車 L
    "narikyou": 4,      # 成香 +L
    "keima": 5,         # 桂馬 N
    "narikei": 6,       # 成桂 +N
    "ginshou": 7,       # 銀將 S
    "narigin": 8,       # 成銀 +S
    "kinshou": 9,       # 金將 G
    "kakugyou": 10,     # 角行 B
    "ryuuma": 11,       # 龍馬 +B
    "hisha": 12,        # 飛車 R
    "ryuuou": 13,       # 龍王 +R
    "gyokushou": -14,   # 玉將 K
    "oushou": 14,       # 王將 K
}


def flip_chessboard(cb: np.ndarray):
    return -cb[::-1]


def rotate_chessboard(cb: np.ndarray):
    return -cb[::-1, ::-1]


def init_chessboard():
    cb = np.zeros([8, 8])

    for _ in range(2):
        cb[-2] = pieces["pawn"]
        cb[-1, 0] = cb[-1, -1] = pieces["rook"]
        cb[-1, 1] = cb[-1, -2] = pieces["knight"]
        cb[-1, 2] = cb[-1, -3] = pieces["bishop"]
        cb[-1, 3] = pieces["queen"]
        cb[-1, 4] = pieces["king"]

        cb = flip_chessboard(cb)

    return cb


def init_chessboard_xq():
    cb = np.zeros([10, 9])

    for _ in range(2):
        for i in range(5):
            cb[-4, i * 2] = pieces_xq["soldier"]

        cb[-3, 1] = cb[-3, -2] = pieces_xq["cannon"]
        cb[-1, 0] = cb[-1, -1] = pieces_xq["chariot"]
        cb[-1, 1] = cb[-1, -2] = pieces_xq["horse"]
        cb[-1, 2] = cb[-1, -3] = pieces_xq["elephant"]
        cb[-1, 3] = cb[-1, -4] = pieces_xq["mandarin"]
        cb[-1, 4] = pieces_xq["general"]

        cb = flip_chessboard(cb)

    return cb


def init_chessboard_sg():
    cb = np.zeros([9, 9])

    for _ in range(2):
        cb[-3] = pieces_sg["fuhyou"]

        cb[-2, 1] = pieces_sg["kakugyou"]
        cb[-2, -2] = pieces_sg["hisha"]

        cb[-1, 0] = cb[-1, -1] = pieces_sg["kyousha"]
        cb[-1, 1] = cb[-1, -2] = pieces_sg["keima"]
        cb[-1, 2] = cb[-1, -3] = pieces_sg["ginshou"]
        cb[-1, 3] = cb[-1, -4] = pieces_sg["kinshou"]
        cb[-1, 4] = pieces_sg["oushou"]

        cb = rotate_chessboard(cb)

    return cb


def main():
    print(init_chessboard_sg())


if __name__ == '__main__':
    main()
