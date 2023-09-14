from environment.card import Card
from params import NUM_PILES

class Action(object):
    """
    Description goes here.
    """

    def __init__(
        self, card: Card, from_: str, to_: str, pile_from: int, pile_to: int
    ) -> None:
        from game import Game
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
        self.game = game
        func_map = {
            ("stock", "talon"):self.stock_to_talon,
            ("stock", "tableau"):self.stock_to_tableau,
            ("stock", "foundation"):self.stock_to_foundation,
            ("tableau", "tableau"):self.tableau_to_tableau,
            ("tableau", "foundation"):self.tableau_to_foundation,
            ("foundation", "tableau"):self.foundation_to_tableau,
        }
        is_valid = func_map.get((self.from_, self.to_), False)
        return is_valid

    def stock_to_talon(self):
        return True

    def stock_to_tableau(self):
        card_in_tableau = self.game.tableau.piles[-1]
        pass

    def stock_to_foundation(self):
        pass

    def tableau_to_tableau(self):
        pass

    def tableau_to_foundation(self):
        pass

    def foundation_to_tableau(self):
        pass

        # if card.movable:
        #     if to_ == -1:  # TOP ROW
        #         if not from_ in range(NUM_PILES) or self.tableau[from_][-1] == card:
        #             symbol = card.symbol
        #             if len(self.foundations[symbol]):
        #                 card_2 = self.foundations[symbol][-1]
        #                 if card.rank == card_2.rank + 1:
        #                     validity = True
        #             else:
        #                 if card.rank == 1:
        #                     validity = True

        #     elif to_ in range(NUM_PILES):  # OTHER COLUMN
        #         symbol = card.symbol
        #         color = COLORS[symbol]
        #         if len(self.tableau[to_]):
        #             card_2 = self.tableau[to_][-1]
        #             color_2 = COLORS[card_2.symbol]

        #             if card.rank == card_2.rank - 1 and 1 - color == color_2:
        #                 validity = True
        #         else:  # KING
        #             if card.rank == max(RANKS):
        #                 validity = True
        #         pass

        #     else:
        #         raise ValueError("Invalid destination")