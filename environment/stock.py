from typing import List
from random import shuffle

from environment.card import Card
from environment.tableau import Tableau


class Stock(object):
    """
    If the entire pack is not laid out in a tableau at the beginning of a game,
    the remaining cards form the stock pile from which additional cards are
    brought into play according to the rules.
    """

    def __init__(self, pack: List[Card]) -> None:
        self.cards: List[Card] = [Card(symbol, rank) for symbol, rank in pack]
        shuffle(self.cards)
        self.index = 0
        pass

    def deal(self, num_piles: int) -> Tableau:
        tableau = Tableau(num_piles=num_piles)
        for i in range(num_piles):
            for _ in range(i + 1):
                tableau.piles[i].append(self.cards[0])
                self.cards.pop(0)
            tableau.piles[i][-1].face_up = True
        return tableau
