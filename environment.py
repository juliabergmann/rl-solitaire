# Imports
from itertools import product
from random import shuffle

# Constants
# clubs (♣), diamonds (♦), hearts (♥), and spades (♠)
SYMBOLS = ["♣", "♠", "♥", "♦"]
COLORS = {"♣": 1, "♠": 1, "♥": 0, "♦": 0}
NOTES = range(1, 14)
DECK = list(product(SYMBOLS, NOTES))
NUM_COLS = 7


# Classes
class Card(object):
    def __init__(self, symbol: str, note: int):
        self.symbol = symbol
        self.note = note
        self.is_known = False
        self.is_final = False
        self.movable = False


class Table(object):
    def __init__(self):
        # Parameters
        self.leftover_index = 0

        # Initialize
        deck = [Card(symbol, note) for symbol, note in DECK]
        # Shuffle
        shuffle(deck)
        # Deal
        self.final_deck = {symbol: [] for symbol in SYMBOLS}
        ind_start = {i: sum(j for j in range(i + 1)) for i in range(NUM_COLS)}
        ind_end = {i: ind_start[i] + i + 1 for i in range(NUM_COLS)}
        self.play_space = {i: deck[ind_start[i] : ind_end[i]] for i in range(NUM_COLS)}
        self.leftover = deck[28:-1]
        self.leftover[0].is_known = True
        self.leftover[0].movable = True
        for column in self.play_space.values():
            column[-1].is_known = True
            column[-1].movable = True

    def __str__(self):
        layout = "\nDEAL:\n"
        for col, column in self.play_space.items():
            layout += f"{col} >> "
            for elem in column:
                if elem.is_known:
                    layout += elem.symbol
                    layout += str(elem.note)
                    layout += " "
                else:
                    layout += "?? "
            layout += "\n"

        layout += "\nLEFTOVER:\n"
        for elem in self.leftover:
            if elem.is_known:
                layout += elem.symbol
                layout += str(elem.note)
                layout += " "
            else:
                layout += "?? "
        layout += "\n"

        layout += "\nTOP ROW:\n"
        for shape, finals in self.final_deck.items():
            layout += shape + ": "
            for elem in finals:
                if elem.is_known:
                    layout += elem.symbol
                    layout += str(elem.note)
                    layout += " "
                else:
                    layout += "?? "
            layout += "\n"
        return layout

    def get_valid_actions(self):
        """
        Collect all the valid actions
        Destination code:
            -1 : top row
            0:NUM_COLS : other columns
        """
        valid_actions = []
        # check from DEAL
        for source_col in range(NUM_COLS):
            # check top row
            destination = -1
            card = self.play_space[source_col][-1]
            if self.check_valid_move(card=card, destination=destination):
                valid_actions.append((card, destination))
            # check other columns
            for destination in range(NUM_COLS):
                if destination == source_col:
                    break
                else:
                    for card in self.play_space[source_col]:
                        if card.is_known and card.movable:
                            if self.check_valid_move(
                                card=card, destination=destination
                            ):
                                valid_actions.append((card, destination))

        # check from LEFTOVER
        # check top row
        destination = -1
        card = self.leftover[self.leftover_index]
        if self.check_valid_move(card=card, destination=destination):
            valid_actions.append((card, destination))
        # check other columns
        for destination in range(NUM_COLS):
            if card.is_known and card.movable:
                if self.check_valid_move(card=card, destination=destination):
                    valid_actions.append((card, destination))

        return valid_actions

    def check_valid_move(self, card: Card, destination: int):
        """
        Check the validity of putting `card_1` on top of `card_2`
        """
        validity = False
        if card.movable:
            if destination == -1:  # TOP ROW
                symbol = card.symbol
                if len(self.final_deck[symbol]):
                    card_2 = self.final_deck[symbol][-1]
                    if card.note == card_2.note + 1:
                        validity = True
                else:
                    if card.note == 1:
                        validity = True

            elif destination < NUM_COLS:  # OTHER COLUMN
                symbol = card.symbol
                color = COLORS[symbol]
                if len(self.play_space[destination]):
                    card_2 = self.play_space[destination][-1]
                    color_2 = COLORS[card_2.symbol]

                    if card.note == card_2.note - 1 and 1 - color == color_2:
                        validity = True
                else:  # KING
                    if card.note == 13:
                        validity = True
                pass

            else:
                raise ValueError("Invalid destination")

        return validity

    def update_table(self, action):
        return None

    def is_game_over(self):
        return None


T = Table()
print(T)
for card, dest in T.get_valid_actions():
    print(card.symbol + str(card.note) + " ---> " + str(dest))
