# Imports
from random import shuffle

# Constants
SYMBOLS = ["C", "D", "H", "S"]
COLORS = {"C": 1, "D": 0, "H": 0, "S": 1}


# Classes
class Card:
    def __init__(self, symbol: str, note: int):
        self.symbol = symbol
        self.note = note
        self.is_known = False
        self.is_final = False
        self.movable = False


class Table:
    def __init__(self):
        deck = []
        for symbol in SYMBOLS:
            for note in range(1, 14):
                deck.append(Card(symbol, note))
        # shuffle(deck)
        self.final_deck = {symbol: [] for symbol in SYMBOLS}
        self.play_space = []
        for i in range(7):
            self.play_space.append([])
            for j in range(i + 1):
                self.play_space[-1].append(deck[0])
                deck.pop(0)
        self.leftover = deck
        self.leftover[0].is_known = True
        self.leftover[0].movable = True
        for column in self.play_space:
            column[-1].is_known = True
            column[-1].movable = True

    def print_table(self):
        for column in self.play_space:
            print(
                [
                    (elem.symbol, elem.note) if elem.is_known else ("?", "?")
                    for elem in column
                ]
            )
        print(
            [
                (elem.symbol, elem.note) if elem.is_known else ("?", "?")
                for elem in self.leftover
            ]
        )
        for shape, finals in self.final_deck.items():
            print(shape)
            print(
                [
                    (elem.symbol, elem.note) if elem.is_known else ("?", "?")
                    for elem in finals
                ]
            )
        return None

    def get_valid_actions(self):
        """
        Collect all the valid actions
        """
        valid_actions = []
        # check finals
        destination = "final_deck"
        for i in range(7):
            card = self.play_space[i][-1]
            if check_valid_move(card=card, table=self, destination=destination):
                valid_actions.append((card, destination))
        return valid_actions


def check_valid_move(card: Card, table: Table, destination: str):
    """
    Check the validity of putting `card_1` on top of `card_2`
    """
    validity = False
    if card.movable:
        if destination == "final_deck":  # when
            symbol = card.symbol
            if len(table.final_deck[symbol]):
                card_2 = table.final_deck[symbol][-1]
                if card.note == card_2.note + 1:
                    validity = True
            else:
                if card.note == 1:
                    validity = True
    return validity


T = Table()
T.print_table()
T.get_valid_actions()
