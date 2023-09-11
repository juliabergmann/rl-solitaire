from params import NUM_COLS
from environment import Table

test = True
while test:
    T = Table()
    print(T)
    for action in T.get_valid_actions():
        card, dest, source = action
        print(f"{card.symbol}{str(card.note)}: {str(source)} ---> {str(dest)}")
        if source in range(NUM_COLS) and dest in range(NUM_COLS):
            T.update_table(action)
            print(T)
            test = False
            break
