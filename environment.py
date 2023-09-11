# Imports
from random import shuffle

from params import DECK, SYMBOLS, NUM_COLS, COLORS

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
            -1  :   top row
            0:7 :   other columns
        Target code:
            -2  :   leftovers
            -1  :   top row
            0:7 :   other columns
        """
        valid_actions = []
        # check from DEAL
        for source_col in range(NUM_COLS):
            # check top row
            destination = -1
            card = self.play_space[source_col][-1]
            if self.check_valid_move(card=card, destination=destination):
                valid_actions.append((card, destination, source_col))
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
                                valid_actions.append((card, destination, source_col))

        # check from LEFTOVER
        # check top row
        destination = -1
        card = self.leftover[self.leftover_index]
        if self.check_valid_move(card=card, destination=destination):
            valid_actions.append((card, destination, -2))
        # check other columns
        for destination in range(NUM_COLS):
            if card.is_known and card.movable:
                if self.check_valid_move(card=card, destination=destination):
                    valid_actions.append((card, destination, -2))

        # drawing from leftover is always an option
        valid_actions.append((card, -2, -2))

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

            elif destination in range(NUM_COLS):  # OTHER COLUMN
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

    def update_table(self, action: tuple[Card, int, int]):
        card, destination, source = action
        symbol = card.symbol
        if source == -2:
            # From deck
            if destination == -2:
                # Nem draw from deck
                self.leftover_index += 1
                self.leftover_index = self.leftover_index % len(self.leftover)
                card.movable = False
            elif destination == -1:
                # To top row
                self.final_deck[symbol].append(card)
                self.leftover.pop(self.leftover_index) # no need to update index!
            elif destination in range(NUM_COLS):
                # To a column
                self.play_space[destination][-1].movable = False
                self.play_space[destination].append(card)
                self.leftover.pop(self.leftover_index) # no need to update index!
                pass
            else:
                raise ValueError("Unknown destination code.")
            # what's under the next field
            self.leftover[self.leftover_index].is_known = True
            self.leftover[self.leftover_index].movable = True

        elif source == -1:
            # TODO
            if destination in range(NUM_COLS):
                # bring something back from top row
                pass
            else:
                raise ValueError("Unknown destination code.")
            
        elif source in range(NUM_COLS):
            if destination == -1:
                # To top row
                self.final_deck[symbol].append(card)
                self.play_space[source].pop(-1) # no need to update index!
                if len(self.play_space[source]):
                    self.play_space[source][-1].movable = True
                    self.play_space[source][-1].is_known = True
                pass
            elif destination in range(NUM_COLS):
                self.play_space[destination][-1].movable = False
                self.play_space[destination].append(card)
                self.play_space[source].pop(-1)
                if len(self.play_space[source]):
                    self.play_space[source][-1].movable = True
                    self.play_space[source][-1].is_known = True
                pass
            else:
                raise ValueError("Unknown destination code.")
            
        else:
            raise ValueError("Unkown source code.")
        return None

    def is_game_over(self):
        value = True
        for finals in self.final_deck.values():
            if len(finals) != 14:
                value = False
        return value
            
