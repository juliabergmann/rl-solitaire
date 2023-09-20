from params import MAX_STEPS
from game import Game
from agent import Player
import numpy as np
import matplotlib.pyplot as plt

"""
Rules:
https://bicyclecards.com/how-to-play/solitaire
"""

if __name__ == "__main__":
    game = Game()
    # print(game)
    player = Player(game, alpha=0.1, random_factor=0.25)
    moveHistory = []
    for i in range(1000):
        if i % 100 == 0:
            print(i)
        game = Game()  # reinitialize the maze
        learn_it = True
        counter = 0
        while not game.is_game_over():
            # print(f"-o-\n\n>>> STEP {game.steps}:")
            allowed_states = game.get_valid_actions()
            if len(allowed_states) == 1:
                counter += 1
            else:
                counter = 0
            action = player.choose_action(
                allowed_states
            )  # choose an action (explore or exploit)
            game.update_table(action)  # update the maze according to the action
            # print(action)
            # print(game)
            state, reward = game.get_state_and_reward()  # get the new state and reward
            player.update_state_history(
                state, reward
            )  # update the robot memory with state and reward
            num_cards_to_roll = len(game.stock.cards) + len(game.talon.cards)
            if game.steps >= MAX_STEPS or counter > num_cards_to_roll*2:
                # end the robot if it takes too long to find the goal
                game.end_game()
                learn_it = False
        if learn_it:
            print(player.reward_dict)
            player.learn()  # robot should learn after every episode
            moveHistory.append(
                game.steps
            )  # get a history of number of steps taken to plot later

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
