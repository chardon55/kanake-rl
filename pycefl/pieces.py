pieces_names = (
    "EMPTY",
    "pawn",         # 🨅
    "rook",         # 🨂
    "knight",       # 🨄
    "bishop",       # 🨃
    "queen",        # 🨁
    "king",         # 🨀
)

pieces_names_xq = (
    "EMPTY",
    "soldier",      # 🩦 🩭
    "cannon",       # 🩥 🩬
    "chariot",      # 🩤 🩫
    "horse",        # 🩣 🩪
    "elephant",     # 🩢 🩩
    "mandarin",     # 🩡 🩨
    "general",      # 🩠 🩧
)

pieces_names_sg = (
    "EMPTY",
    "pawn",             # 歩兵 P
    "ppawn",            # と金 +P
    "lance",            # 香車 L
    "plance",           # 成香 +L
    "knight",           # 桂馬 N
    "pknight",          # 成桂 +N
    "silver",           # 銀將 S
    "psilver",          # 成銀 +S
    "gold",             # 金將 G
    "bishop",           # 角行 B
    "pbishop",          # 龍馬 +B
    "rook",             # 飛車 R
    "prook",            # 龍王 +R
    "king",             # 王將/玉將 K
)


def __init_dict(name_tuple) -> dict:
    return {k: v for v, k in enumerate(name_tuple)}


pieces = __init_dict(pieces_names)
pieces_xq = __init_dict(pieces_names_xq)
pieces_sg = __init_dict(pieces_names_sg)

pieces_count = (None, 8, 2, 2, 2, 1, 1)
pieces_xq_count = (None, 5, 2, 2, 2, 2, 2, 1)
piece_sg_count = (None, 9, 0, 2, 0, 2, 0, 1, 0, 1, 1, 0, 1, 0, 1)
