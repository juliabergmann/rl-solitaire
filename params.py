from itertools import product


# Constants
# clubs (♣), diamonds (♦), hearts (♥), and spades (♠)
SYMBOLS = ["♣", "♠", "♥", "♦"]
COLORS = {"♣": 1, "♠": 1, "♥": 0, "♦": 0}
NOTES = range(1, 14)
DECK = list(product(SYMBOLS, NOTES))
NUM_COLS = 7
