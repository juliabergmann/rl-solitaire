from environment.card import Card
from params import NUM_PILES

class Action(object):
    """
    Description goes here.
    """

    def __init__(
        self, card: Card, from_: str, to_: str, pile_from: int, pile_to: int
    ) -> None:
        self.card = card
        self.from_ = from_
        self.to_ = to_
        self.pile_from = pile_from
        self.pile_to = pile_to
        self.check_inputs()
        pass

    def check_inputs(self):
        valid_string_pairs = (
            ("stock", "talon"),
            ("stock", "tableau"),
            ("stock", "foundation"),
            ("tableau", "tableau"),
            ("tableau", "foundation"),
            ("foundation", "tableau"),
        )
        if (self.from_, self.to_) not in valid_string_pairs:
            raise ValueError("Not valid action: STRING error.")

        if self.from_ == "tableau" and self.pile_from not in range(NUM_PILES):
            raise ValueError("Not valid action: FROM error.")

        if self.to_ == "tableau" and self.pile_to not in range(NUM_PILES):
            raise ValueError("Not valid action: TO error.")

    def check_validity(self, game):
        from game import Game
        self.game: Game = game
        func_map = {
            "talon":self.to_talon,
            "tableau":self.to_tableau,
            "foundation":self.to_foundation,
        }
        is_valid = func_map.get(self.to_, False)
        return is_valid

    def to_talon(self):
        # It's always allowed.
        return True

    def to_tableau(self):
        # Check the target card
        card_to = self.game.tableau.piles[self.pile_to][-1]
        # If they haev the same color, it's NO-NO
        if self.card.color == card_to.color:
            return False
        # If the ranks don't match, it's NO-No
        if self.card.rank != card_to.rank + 1:
            return False
        # Otherwise: GO-GO :-)
        return True

    def to_foundation(self):
        # When we pick from tableau, it must be the last card:
        if self.from_ == "tableau":
            if self.game.tableau.piles[self.pile_from][-1] != self.card:
                return False
        # Otherwise, we check the foundation:
        symbol = self.card.symbol
        # If the foundation already has cards:
        if len(self.game.foundations[symbol]):
            # get the last card of the foundation
            last_card = self.game.foundations[symbol].last_card()
            # check if the ranks are correct:
            if self.card.rank == last_card.rank + 1:
                return True
        # If the foundation is empty:
        else:
            # the card's rank must be 1
            if self.card.rank == 1:
                return True
        return False
