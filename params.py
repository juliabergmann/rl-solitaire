from itertools import product


# Constants
# clubs (♣), diamonds (♦), hearts (♥), and spades (♠)
SYMBOLS = ["♣", "♠", "♥", "♦"]
COLORS = {"♣": 1, "♠": 1, "♥": 0, "♦": 0}
NOTES = range(1, 14)
DECK = list(product(SYMBOLS, NOTES))
NUM_COLS = 7
MAX_STEPS = 1000


def allmax(a):
    if len(a) == 0:
        return []
    all_ = [0]
    max_ = a[0]
    for i in range(1, len(a)):
        if a[i] > max_:
            all_ = [i]
            max_ = a[i]
        elif a[i] == max_:
            all_.append(i)
    return all_