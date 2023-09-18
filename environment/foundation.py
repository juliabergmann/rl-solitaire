from typing import List

from environment.card import Card


class Foundation(object):
    """
    Four piles on which a whole suit or sequence must be built up.
    In most Solitaire games, the four aces are the bottom card or base of the foundations.
    The foundation piles are clubs (♣), diamonds (♦), hearts (♥), and spades (♠).
    """

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.pile: List[Card] = []
        self.complete: bool = False
        pass

    def last_card(self) -> Card:
        try:
            return self.pile[-1]
        except:
            return None

    def num_of_cards(self) -> int:
        return len(self.pile)
