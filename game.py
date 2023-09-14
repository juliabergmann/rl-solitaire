# Imports
from typing import List, Dict

from params import PACK, SYMBOLS, RANKS, NUM_PILES, COLORS
from environment.stock import Stock
from environment.foundation import Foundation
from environment.card import Card
from environment.tableau import Tableau
from environment.talon import Talon


# Game
class Game(object):
    def __init__(self):
        # Parameters
        self.leftover_index = 0
        self.steps = 0
        # Initialize
        self.foundations: Dict[str, Foundation] = {
            symbol: Foundation(symbol=symbol) for symbol in SYMBOLS
        }
        self.stock: Stock = Stock(pack=PACK)
        # Deal
        self.tableau: Tableau = self.stock.deal(num_piles=NUM_PILES)
        self.stock.cards[0].face_up = True
        self.talon = Talon()
        return

    def get_valid_actions(self):
        """
        Collect all the valid actions
        Destination code:
            -1  :   top row
            0:7 :   other columns
        Source code:
            -2  :   leftovers
            -1  :   top row
            0:7 :   other columns
        """
        valid_actions = []
        # check from DEAL
        for source_col in range(NUM_PILES):
            if len(self.tableau[source_col]):
                # check top row
                destination = -1
                card = self.tableau[source_col][-1]
                if self.check_valid_move(
                    card=card, destination=destination, source=source_col
                ):
                    valid_actions.append((card, destination, source_col))
                # check other columns
                for destination in range(NUM_PILES):
                    if destination == source_col:
                        break
                    else:
                        for card in self.tableau[source_col]:
                            if card.face_up and card.movable:
                                if self.check_valid_move(
                                    card=card,
                                    destination=destination,
                                    source=source_col,
                                ):
                                    valid_actions.append(
                                        (card, destination, source_col)
                                    )

        # check from LEFTOVER
        # check top row
        if len(self.stock):
            destination = -1
            source = -2
            card = self.stock[self.leftover_index]
            if self.check_valid_move(card=card, destination=destination, source=source):
                valid_actions.append((card, destination, source))
            # check other columns
            for destination in range(NUM_PILES):
                if card.face_up and card.movable:
                    if self.check_valid_move(
                        card=card, destination=destination, source=source
                    ):
                        valid_actions.append((card, destination, source))

        # drawing from stock is always an option
        valid_actions.append((card, -2, -2))

        return valid_actions

    def check_valid_move(self, card: Card, destination: int, source: int):
        """
        Check the validity of putting `card_1` on top of `card_2`
        """
        validity = False
        if card.movable:
            if destination == -1:  # TOP ROW
                if not source in range(NUM_PILES) or self.tableau[source][-1] == card:
                    symbol = card.symbol
                    if len(self.foundations[symbol]):
                        card_2 = self.foundations[symbol][-1]
                        if card.rank == card_2.rank + 1:
                            validity = True
                    else:
                        if card.rank == 1:
                            validity = True

            elif destination in range(NUM_PILES):  # OTHER COLUMN
                symbol = card.symbol
                color = COLORS[symbol]
                if len(self.tableau[destination]):
                    card_2 = self.tableau[destination][-1]
                    color_2 = COLORS[card_2.symbol]

                    if card.rank == card_2.rank - 1 and 1 - color == color_2:
                        validity = True
                else:  # KING
                    if card.rank == max(RANKS):
                        validity = True
                pass

            else:
                raise ValueError("Invalid destination")

        return validity

    def update_table(self, action: tuple[Card, int, int]):
        self.steps += 1
        card, destination, source = action
        symbol = card.symbol
        if source == -2:
            # From deck
            if destination == -2:
                # Nem draw from deck
                self.leftover_index += 1
                card.movable = False
            elif destination == -1:
                # To top row
                self.foundations[symbol].append(card)
                self.stock.pop(self.leftover_index)  # no need to update index!
            elif destination in range(NUM_PILES):
                # To a column
                # if len(self.tableau[destination]):
                #     self.tableau[destination][-1].movable = False
                self.tableau[destination].append(card)
                self.stock.pop(self.leftover_index)  # no need to update index!
                pass
            else:
                raise ValueError("Unknown destination code.")
            # what's under the next field
            if len(self.stock):
                self.leftover_index = self.leftover_index % len(self.stock)
                self.stock[self.leftover_index].face_up = True
                self.stock[self.leftover_index].movable = True

        elif source == -1:
            # TODO
            if destination in range(NUM_PILES):
                # bring something back from top row
                pass
            else:
                raise ValueError("Unknown destination code.")

        elif source in range(NUM_PILES):
            if destination == -1:
                # To top row
                self.foundations[symbol].append(card)
                self.tableau[source].pop(-1)  # no need to update index!
                if len(self.tableau[source]):
                    self.tableau[source][-1].movable = True
                    self.tableau[source][-1].face_up = True
                pass
            elif destination in range(NUM_PILES):
                # TODO: most még csak az utolsó lapot tudja arrébb rakni
                # if len(self.tableau[destination]):
                #     self.tableau[destination][-1].movable = False
                card_index = self.tableau[source].index(card)
                for item in self.tableau[source][card_index:]:
                    self.tableau[destination].append(item)
                self.tableau[source] = self.tableau[source][:card_index]
                if len(self.tableau[source]):
                    self.tableau[source][-1].movable = True
                    self.tableau[source][-1].face_up = True
                pass
            else:
                raise ValueError("Unknown destination code.")

        else:
            raise ValueError("Unkown source code.")
        return None

    def is_game_over(self):
        value = True
        for finals in self.foundations.values():
            if len(finals) != len(RANKS):
                value = False
        return value

    def give_reward(self):
        num_of_known_cards = 0
        for card in self.stock:
            if card.face_up:
                num_of_known_cards += 1
        for col in self.tableau.values():
            for card in col:
                if card.face_up:
                    num_of_known_cards += 1
        return num_of_known_cards

    def get_state_and_reward(self):
        return self, self.give_reward()

    def end_game(self):
        for key, _ in self.foundations.items():
            self.foundations[key] = RANKS
        return None

    def __str__(self):
        layout = "\nFOUNDATIONS:\n"
        for symbol, foundation in self.foundations.items():
            layout += symbol + ": "
            for card in foundation.pile:
                if card.face_up:
                    layout += card.symbol
                    layout += str(card.rank)
                    layout += " "
                else:
                    layout += "[] "
            layout += "\n"

        layout += "\nTABLEAU:\n"
        for col, column in self.tableau.piles.items():
            layout += f"{col} >> "
            for card in column:
                if card.face_up:
                    layout += card.symbol
                    layout += str(card.rank)
                    layout += " "
                else:
                    layout += "[] "
            layout += "\n"

        layout += "\nSTOCK:\n"
        for card in self.stock.cards:
            if card.face_up:
                layout += card.symbol
                layout += str(card.rank)
                layout += " "
            else:
                layout += "[] "
        layout += "\n"

        layout += "\nTALON:\n"
        for card in self.talon.cards:
            if card.face_up:
                layout += card.symbol
                layout += str(card.rank)
                layout += " "
            else:
                layout += "[] "
        layout += "\n"

        return layout
