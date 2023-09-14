from random import random

import numpy as np

from game import Game
from params import NUM_PILES
from auxiliary import allmax


class Player(object):
    def __init__(
        self, table: Game, alpha: float = 0.15, random_factor: float = 0.2
    ) -> None:
        self.state_history = [(table, 0)]
        self.alpha = alpha
        self.random_factor = random_factor
        pass

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        # TODO: how to learn
        # target = 0  # we know the "ideal" reward
        # a = self.alpha
        # for state, reward in reversed(self.state_history):
        #     self.G[state] = self.G[state] + a * (target - self.G[state])
        # self.state_history = []  # reset the state_history
        self.random_factor -= 10e-5  # decrease random_factor

    def choose_action(self, allowed_moves):
        if len(allowed_moves) == 1:
            next_move = allowed_moves[0]
        else:
            allowed_moves = np.array(allowed_moves)
            next_move = None
            rand = random()
            if rand < self.random_factor:
                choice = np.random.choice(range(len(allowed_moves)))
                next_move = allowed_moves[choice]
            else:
                rewards = []
                for action in allowed_moves:
                    _, destination, source = action
                    rewards.append(0)
                    if destination == -1:
                        rewards[-1] += 2
                    if source in range(NUM_PILES):
                        rewards[-1] += 1
                max_places = allmax(rewards)
                # print(f"moves: {allowed_moves}")
                # print(f"rewards: {rewards}")
                # print(f"argmaxs: {max_places}")
                choice = np.random.choice(max_places)
                next_move = allowed_moves[choice]
                # print(f"next: {next_move}")
        return next_move
