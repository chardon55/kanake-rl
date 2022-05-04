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
    "fuhyou",           # 歩兵 P
    "tokin",            # と金 +P
    "kyousha",          # 香車 L
    "narikyou",         # 成香 +L
    "keima",            # 桂馬 N
    "narikei",          # 成桂 +N
    "ginshou",          # 銀將 S
    "narigin",          # 成銀 +S
    "kinshou",          # 金將 G
    "kakugyou",         # 角行 B
    "ryuuma",           # 龍馬 +B
    "hisha",            # 飛車 R
    "ryuuou",           # 龍王 +R
    "shou",             # 王將/玉將 K
)


def __init_dict(name_tuple) -> dict:
    return {k: v for v, k in enumerate(name_tuple)}


pieces = __init_dict(pieces_names)
pieces_xq = __init_dict(pieces_names_xq)
pieces_sg = __init_dict(pieces_names_sg)
