from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import tensorflow as tf
import time
import random
import os
import numpy as np

from Encoding_Module.environment import Environment


MODEL_NAME = "Planning"
REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE = 64
DISCOUNT = 0.99
UPDATE_TARGET_EVERY = 5
MIN_REWARD = -200
MEMORY_FRACTION = 0.2

# Environment settings
EPISODES = 20_000

# Exploration settings
epsilon = 1  # Not a constant, going to be decayed
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

# Stats settings
AGGREGATE_STATS_EVERY = 50  # Episodes



# For stats
ep_rewards = [-200]

# For more repetitive results
random.seed(1)
np.random.seed(1)
tf.set_random_seed(1)

# Create models folder
if not os.path.isdir('models'):
    os.makedirs('models')


# Own Tensorboard class
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.FileWriter(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

class DQNAgent:

    def __init__(self, env):
        self.env = env

        # Main model. The one that gets trained every step
        self.model = self.create_model()

        # Target model. The one we .predict against every step
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        self.tensorboard = ModifiedTensorBoard(log_dir=f"log/{MODEL_NAME}-{int(time.time())}")
        self.target_update_counter = 0

    def create_model(self):
        model = Sequential()

        model.add(Flatten())
        model.add(Dense(units=500, activation="relu"))
        model.add(Dense(units=5000, activation="relu"))
        model.add(Dense(units=50000, activation="relu"))
        model.add(Dense(units=len(self.env.allActions), activation="softmax"))

        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])

        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(np.array(state))[0]

    def train(self, terminal_state, step):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get MINIBATCH_SIZE random samples from replay_memory
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Transition: (current_state, action, reward, new_current_state, done)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False, callbacks=[self.tensorboard] if terminal_state else None)

        # Updating to determine if we want to update target_model yet
        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

# -------------------------------------------------------------------------------------------------------------------- #

env = Environment()
agent = DQNAgent(env)

for episode in range(1, EPISODES+1):
    agent.tensorboard.step = episode

    episode_reward = 0
    step = 1
    done = False
    current_state = env.reset()  # TODO: THE STATE SHOULD BE A LIST/ARRAY, NOT A DICTIONARY

    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(agent.get_qs(current_state))  # Integer
        else:
            action = env.sample()  # String

        new_state, reward, done = env.step(action)

        episode_reward += reward

        agent.update_replay_memory((current_state, action, reward, new_state, done))  # TODO: CHECK THIS - Action should be an Integer here
        agent.train(done, step)

        current_state = new_state
        step += 1

    # TODO: CHECK HOW THE TENSOR-BOARD STATS WORK
    # Append episode reward to a list and log stats (every given number of episodes)
    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

        # Save model, but only when min reward is greater or equal a set value
        if min_reward >= MIN_REWARD:
            agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

    # Decay epsilon
    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)

# TODO:
#  - PROBLEM 0: I CANNOT IMPLEMENT THE STANDARD Q-LEARNING METHOD BECAUSE THE STATE VECTOR ENCODING IS TOO BIG AND THERE'S A VAST OBS. AND ACTION SPACE -->
#               Q-TABLE WOULD BE TOO LARGE FOR THIS ALG. TO WORK PROPERLY -->
#               ALTERNATIVE: DEEP Q LEARNING
#  .
#  - PROBLEM 1: WE HAVE A LARGE DISCRETE ACTION SPACE AND WE ARE ONLY INTERESTED IN THE LEGAL ACTIONS
#  .
#       IT IS NOT POSSIBLE TO ADAPT THE SOFTMAX ACTIVATION FUNC. SO IT GIVES 0 PROB TO ILLEGAL ACTIONS ???
#       I CAN GIVE A BIG NEGATIVE REWARD TO ILLEGAL ACTIONS CHOSEN THROUGH GET_QS OR
#       -->  I CAN MAKE THE ARGMAX SELECTION AMONG THE LEGAL ACTIONS  <--
#       ALTERNATIVE: ACTOR-CRITIC ALG. ???
#  .
#  - PROBLEM 2: IN OUR CASE THE REWARD IS OBTAINED ONLY AT THE TERMINAL/GOAL STATE
#  .
#       IN FACT, WE CAN DEFINE A NEGATIVE REWARD BASED ON THE TOTAL COST AND THE INCREASE COMMAND
#       WHAT REWARD DO WE GIVE TO THE GOAL STATE ??? 0 OR A LARGE POSITIVE NUMBER ???
#       WHAT REWARD DO WE GIVE TO THE ACTIONS THAT DO NOT INCLUDE THE INCREASE COMMAND ???
#  .
