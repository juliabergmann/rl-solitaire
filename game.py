# Imports
from typing import List, Dict

import numpy as np

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

    def update_table(self, action: Action):
        """
        Perform a valid action.
        Possible actions:
            - stock         ->  talon           (Note: always valid.)
            - stock         ->  tableau
            - stock         ->  foundation
            - tableau       ->  tableau
            - tableau       ->  foundation
            - foundation    ->  tableau
        """
        # TODO
        self.steps += 1
        symbol = action.card.symbol

        # FROM STOCK ...
        if action.from_ == "stock":
            # ... TO TALON
            if action.to_ == "talon":
                self.talon.cards.append(action.card)
            # ... TO TABLEAU
            if action.to_ == "tableau":
                self.tableau.piles[action.pile_to].append(action.card)
            # ... TO FOUNDATION
            if action.to_ == "foundation":
                self.foundations[symbol].pile.append(action.card)
            self.stock.cards.pop(0)
            # refresh stock
            if not len(self.stock.cards):  # if empty
                self.stock.cards = self.talon.cards.copy()
                self.talon.cards = []
                for card in self.stock.cards:
                    card.face_up = False
            if len(self.stock.cards):
                self.stock.cards[0].face_up = True

        # FROM TABLEAU ...
        if action.from_ == "tableau":
            # ... TO TABLEAU
            if action.to_ == "tableau":
                index = self.tableau.piles[action.pile_from].index(action.card)
                self.tableau.piles[action.pile_to] += self.tableau.piles[
                    action.pile_from
                ][index:]
                self.tableau.piles[action.pile_from] = self.tableau.piles[
                    action.pile_from
                ][:index]
                pass
            # ... TO FOUNDATION
            if action.to_ == "foundation":
                self.foundations[symbol].pile.append(action.card)
                self.tableau.piles[action.pile_from].pop(-1)
                pass
            # check if new card can be turned over
            try:
                next_card = self.tableau.piles[action.pile_from][-1]
                next_card.face_up = True
            except:
                pass

        # FROM FOUNDATION ...
        if action.from_ == "foundation":
            # ... TO TABLEAU
            if action.to_ == "tableau":
                self.tableau.piles[action.pile_to].append(action.card)
                self.foundations[symbol].pile.pop(-1)
                pass

        return None

    def is_game_over(self):
        for foundation in self.foundations.values():
            if not foundation.complete:
                return False
        return True

    def give_reward(self):
        """
        sum of cards in foundation minus the std between the piles
        """
        num_in_foundation = [
            foundation.num_of_cards() for foundation in self.foundations.values()
        ]
        reward = sum(num_in_foundation)
        reward -= np.std(num_in_foundation)
        return reward

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
