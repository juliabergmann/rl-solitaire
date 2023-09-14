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
        if self.pile_from not in range(NUM_PILES) or self.pile_to not in range(
            NUM_PILES
        ):
            raise ValueError("Not valid action: INTEGER error.")
