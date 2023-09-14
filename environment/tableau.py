from typing import Dict, List
from environment.card import Card


class Tableau(object):
    """
    Some piles that make up the main table.
    """

    def __init__(self, num_piles: int) -> None:
        self.piles: Dict[int, List[Card]] = {i: [] for i in range(num_piles)}
        pass
