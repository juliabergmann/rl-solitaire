from itertools import product


# Constants
# clubs (♣), diamonds (♦), hearts (♥), and spades (♠)
SYMBOLS = ["♣", "♠", "♥", "♦"]
COLORS = {"♣": 1, "♠": 1, "♥": 0, "♦": 0}
RANKS = range(1, 5)
PACK = list(product(SYMBOLS, RANKS))
NUM_PILES = 2
MAX_STEPS = 2000
