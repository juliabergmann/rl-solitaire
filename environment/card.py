from params import COLORS


class Card(object):
    """
    The symbol of the Card is clubs (♣), diamonds (♦), hearts (♥), or spades (♠).
    The rank of the Card is from 1 to 13.
    During the game the card can be face up or face down.
    """

    def __init__(self, symbol: str, rank: int):
        self.symbol = symbol
        self.color = COLORS[symbol]
        self.rank = rank
        self.face_up = False
        self.movable = False
        pass
