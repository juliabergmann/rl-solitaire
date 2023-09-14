# Imports
from typing import List, Dict

from params import PACK, SYMBOLS, RANKS, NUM_PILES, COLORS
from environment.stock import Stock
from environment.foundation import Foundation
from environment.card import Card
from environment.tableau import Tableau
from environment.talon import Talon
from environment.action import Action


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
        Collect all the valid actions.
        Possible actions:
            - stock         ->  talon           (Note: always valid.)
            - stock         ->  tableau
            - stock         ->  foundation
            - tableau       ->  tableau
            - tableau       ->  foundation
            - foundation    ->  tableau
        """
        card: Card
        valid_actions: List[Action] = []
        action: Action
        # FROM STOCK ...
        if len(self.stock.cards):
            card = self.stock.cards[0]
            ## ... TO TALON
            action = Action(card=card, from_="stock", to_="talon")
            if self.check_validity(action):
                valid_actions.append(action)
            ## ... TO TABLEAU
            for pile_to in range(NUM_PILES):
                action = Action(
                    card=card,
                    from_="stock",
                    to_="tableau",
                    pile_to=pile_to,
                )
                if self.check_validity(action):
                    valid_actions.append(action)
            ## ... TO FOUNDATION
            action = Action(card=card, from_="stock", to_="foundation")
            if self.check_validity(action):
                valid_actions.append(action)

        # FROM TABLEAU ...
        for pile_from in range(NUM_PILES):
            if len(self.tableau.piles[pile_from]):
                card = self.tableau.piles[pile_from][-1]
                ## ... TO TABLEAU
                for pile_to in range(NUM_PILES):
                    if pile_from == pile_to:
                        break
                    else:
                        for card in self.tableau.piles[pile_from]:
                            if card.face_up:
                                action = Action(
                                    card=card,
                                    from_="tableau",
                                    to_="tableau",
                                    pile_from=pile_from,
                                    pile_to=pile_to,
                                )
                                if self.check_validity(action):
                                    valid_actions.append(action)
                ## ... TO FOUNDATION
                action = Action(
                    card=card,
                    from_="tableau",
                    to_="foundation",
                    pile_from=pile_from,
                )
                if self.check_validity(action):
                    valid_actions.append(action)

        # FROM FOUNDATION ...
        for foundation in self.foundations.values():
            if len(foundation.pile):
                card = foundation.pile[-1]
                ## ... TO TABLEAU
                for pile_to in range(NUM_PILES):
                    action = Action(
                        card=card,
                        from_="foundation",
                        to_="tableau",
                        pile_to=pile_to,
                    )
                    if self.check_validity(action):
                        valid_actions.append(action)

        return valid_actions

    def check_validity(self, action: Action):
        """
        Check the validity of the action.
        """
        return action.check_validity(game=self)

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
        for foundation in self.foundations.values():
            if not foundation.complete:
                return False
        return True

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
        for foundation in self.foundations.values():
            foundation.complete = True
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
