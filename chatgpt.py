import tensorflow as tf
import numpy as np


# Define the solitaire environment
class SolitaireEnv:
    def __init__(self):
        self.deck = np.random.permutation(
            ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4
        )
        self.tableau = [[] for _ in range(7)]
        self.foundation = {
            suit: [] for suit in ["hearts", "diamonds", "clubs", "spades"]
        }
        self.stock = self.deck[:24]
        self.waste = []

    def reset(self):
        self.__init__()
        return self.get_state()

    def get_state(self):
        state_encoding = []
        for pile in self.tableau:
            encoded_pile = [self.encode_card(card) for card in pile]
            state_encoding.append(encoded_pile)
        for suit, pile in self.foundation.items():
            encoded_pile = [self.encode_card(card) for card in pile]
            state_encoding.append(encoded_pile)
        state_encoding.append([self.encode_card(card) for card in self.stock])
        state_encoding.append([self.encode_card(card) for card in self.waste])
        flattened_state = [item for sublist in state_encoding for item in sublist]
        state_array = np.array(flattened_state, dtype=np.float32)
        return state_array

    def step(self, action):
        reward = 0
        done = False

        if action >= 0 and action < 7:
            tableau_pile = self.tableau[action]

            if tableau_pile:
                card = tableau_pile[-1]
                suit, rank = card[:-1], card[-1]

                if len(self.foundation[suit]) == 0 and rank == "A":
                    self.foundation[suit].append(card)
                    tableau_pile.pop()
                elif len(self.foundation[suit]) > 0 and self.is_next_rank(
                    self.foundation[suit][-1], rank
                ):
                    self.foundation[suit].append(card)
                    tableau_pile.pop()
                else:
                    reward = -1
            else:
                reward = -1

        if all(len(pile) == 0 for pile in self.tableau):
            done = True

        return self.get_state(), reward, done

    def is_next_rank(self, card1, rank2):
        ranks = "23456789XJQKA"
        return ranks.index(card1[-1]) + 1 == ranks.index(rank2)

    def encode_card(self, card):
        suits = ["hearts", "diamonds", "clubs", "spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        if not card or len(card) == 0:
            # Handle empty card or card with zero length
            return np.zeros(len(suits) + len(ranks), dtype=np.float32)

        suit_index = suits.index(card[:-1]) if card[:-1] in suits else 0
        rank_index = ranks.index(card[-1]) if card[-1] in ranks else 0

        # One-hot encode the suit and rank
        one_hot_suit = np.zeros(len(suits))
        one_hot_suit[suit_index] = 1.0

        one_hot_rank = np.zeros(len(ranks))
        one_hot_rank[rank_index] = 1.0

        # Combine the one-hot vectors
        encoded_card = np.concatenate((one_hot_suit, one_hot_rank))

        return encoded_card


# Define the Q-network
class QNetwork(tf.keras.Model):
    def __init__(self, num_actions):
        super(QNetwork, self).__init__()
        self.dense1 = tf.keras.layers.Dense(128, activation="relu")
        self.dense2 = tf.keras.layers.Dense(64, activation="relu")
        self.output_layer = tf.keras.layers.Dense(num_actions, activation="linear")

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        return self.output_layer(x)


# Define the Deep Q-Network (DQN) agent
class DQNAgent:
    def __init__(self, num_actions):
        self.num_actions = num_actions
        self.q_network = QNetwork(num_actions)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    def choose_action(self, state, epsilon):
        if np.random.rand() < epsilon:
            return np.random.choice(self.num_actions)
        else:
            q_values = self.q_network(state)
            return np.argmax(q_values)

    def train(self, state, action, next_state, reward, done):
        with tf.GradientTape() as tape:
            q_values = self.q_network(state)
            target = reward + (1 - done) * 0.95 * np.max(self.q_network(next_state))
            action_mask = tf.one_hot(action, self.num_actions)
            loss = tf.reduce_sum(
                tf.square(target - tf.reduce_sum(action_mask * q_values, axis=1))
            )

        gradients = tape.gradient(loss, self.q_network.trainable_variables)
        self.optimizer.apply_gradients(
            zip(gradients, self.q_network.trainable_variables)
        )


# Hyperparameters
num_actions = 7
epsilon_initial = 1.0
epsilon_decay = 0.995
epsilon_min = 0.1
learning_rate = 0.001

# Create the solitaire environment and the DQN agent
env = SolitaireEnv()
agent = DQNAgent(num_actions)

# Training loop
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        epsilon = max(epsilon_min, epsilon_initial * epsilon_decay**episode)
        action = agent.choose_action(state, epsilon)
        next_state, reward, done = env.step(action)
        agent.train(state, action, next_state, reward, done)
        state = next_state
        total_reward += reward

    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

# Evaluate the trained agent
num_eval_episodes = 100
total_eval_rewards = 0

for eval_episode in range(num_eval_episodes):
    state = env.reset()
    eval_done = False

    while not eval_done:
        action = agent.choose_action(state, epsilon=0.0)
        next_state, reward, eval_done = env.step(action)
        state = next_state
        total_eval_rewards += reward

average_eval_reward = total_eval_rewards / num_eval_episodes
print(f"Average Evaluation Reward: {average_eval_reward}")
