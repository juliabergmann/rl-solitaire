from typing import List

from environment.card import Card


class Talon(object):
    """
    Cards from the stock pile that have no place in the tableau or on foundations
    are laid face up in the waste pile.
    """

    def __init__(self) -> None:
        self.cards: List[Card] = []
        pass
