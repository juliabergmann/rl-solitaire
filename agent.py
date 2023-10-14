from typing import Dict

import numpy as np

from game import Game
from params import NUM_PILES
from auxiliary import allmax


class Player(object):
    def __init__(
        self, game: Game, alpha: float = 0.15, random_factor: float = 0.05
    ) -> None:
        self.state_history = [(game, 0)]
        self.alpha = alpha
        self.random_factor = random_factor

        self.state: Game
        self.reward_dict: Dict[(str, str):float] = {
            ("stock", "talon"): -3,
            ("stock", "tableau"): -2,
            ("stock", "foundation"): 0,
            ("tableau", "tableau"): -1,
            ("tableau", "foundation"): 0,
            ("foundation", "tableau"): -0.5,
        }
        pass

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        # TODO: how to learn
        target = 0  # we know the "ideal" reward
        a = self.alpha
        for key, value in self.reward_dict.items():
            self.reward_dict[key] = value + a * (target - value)
        self.state_history = []  # reset the state_history
        self.random_factor -= 10e-5  # decrease random_factor

    def choose_action(self, allowed_moves):
        if len(allowed_moves) == 0:
            print(self.state)
        elif len(allowed_moves) == 1:
            next_move = allowed_moves[0]
        else:
            allowed_moves = np.array(allowed_moves)
            next_move = None
            rand = np.random.random()
            # print(f"Random: {round(rand, 3)}")
            if rand < self.random_factor:
                next_move = np.random.choice(allowed_moves)
            else:
                rewards = []
                for action in allowed_moves:
                    r = self.reward_dict[(action.from_, action.to_)]
                    rewards.append(r)
                max_places = allmax(rewards)
                choice = np.random.choice(max_places)
                next_move = allowed_moves[choice]
        return next_move
