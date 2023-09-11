from params import NUM_COLS
from environment import Table
from agent import Player
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    table = Table()
    player = Player(table, alpha=0.1, random_factor=0.25)
    moveHistory = []
    for i in range(1000):
        if i % 100 == 0:
            print(i)

        while not table.is_game_over():
            state, reward = table.get_state_and_reward()  # get the current state
            allowed_states = table.get_valid_actions()
            action = player.choose_action(
                allowed_states
            )  # choose an action (explore or exploit)
            table.update_table(action)  # update the maze according to the action
            # print(table)
            state, reward = table.get_state_and_reward()  # get the new state and reward
            player.update_state_history(
                state, reward
            )  # update the robot memory with state and reward
            if table.steps > 1000:
                # end the robot if it takes too long to find the goal
                table.end_game()

        player.learn()  # robot should learn after every episode
        moveHistory.append(
            table.steps
        )  # get a history of number of steps taken to plot later
        table = Table()  # reinitialize the maze

plt.semilogy(moveHistory, "o")
plt.savefig("img.png")


# test = True
# while test:
#     T = Table()
#     print(T)
#     for action in T.get_valid_actions():
#         card, dest, source = action
#         print(f"{card.symbol}{str(card.note)}: {str(source)} ---> {str(dest)}")
#         if source in range(NUM_COLS) and dest in range(NUM_COLS):
#             T.update_table(action)
#             print(T)
#             test = False
#             break
