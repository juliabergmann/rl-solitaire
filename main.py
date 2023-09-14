from params import NUM_PILES, MAX_STEPS
from game import Game
from agent import Player
import numpy as np
import matplotlib.pyplot as plt

"""
Rules:
https://bicyclecards.com/how-to-play/solitaire
"""

if __name__ == "__main__":
    table = Game()
    player = Player(table, alpha=0.1, random_factor=0.25)
    moveHistory = []
    for i in range(1):
        if i % 100 == 0:
            print(i)
        counter = 0
        while not table.is_game_over():
            state, reward = table.get_state_and_reward()  # get the current state
            allowed_states = table.get_valid_actions()
            if len(allowed_states) == 1:
                counter += 1
            else:
                counter = 0
            action = player.choose_action(
                allowed_states
            )  # choose an action (explore or exploit)
            table.update_table(action)  # update the maze according to the action
            print(f"-o-\n\n>>> STEP {table.steps}:")
            print(table)
            state, reward = table.get_state_and_reward()  # get the new state and reward
            player.update_state_history(
                state, reward
            )  # update the robot memory with state and reward
            if table.steps >= MAX_STEPS or counter > len(table.stock):
                # end the robot if it takes too long to find the goal
                table.end_game()

        player.learn()  # robot should learn after every episode
        moveHistory.append(
            table.steps
        )  # get a history of number of steps taken to plot later
        table = Game()  # reinitialize the maze

plt.semilogy(moveHistory, "o")
plt.savefig("img.png")


# test = True
# while test:
#     T = Game()
#     print(T)
#     for action in T.get_valid_actions():
#         card, dest, source = action
#         print(f"{card.symbol}{str(card.rank)}: {str(source)} ---> {str(dest)}")
#         if source in range(NUM_PILES) and dest in range(NUM_PILES):
#             T.update_table(action)
#             print(T)
#             test = False
#             break
