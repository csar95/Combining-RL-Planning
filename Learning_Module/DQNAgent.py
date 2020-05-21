from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import time
import random
import numpy as np

from hyperparameters_DQL import *
from utils import *


class DQNAgent:

    def __init__(self, env):
        self.env = env

        # Main model. The one that gets trained every step
        self.model = self.create_model()

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        # self.tensorboard = TensorBoard(log_dir=f"log/{MODEL_NAME}-{int(time.time())}")

    def create_model(self):
        model = Sequential()

        model.add(Dense(units=32,
                        activation="relu",
                        input_dim=self.env.state.size)),
        model.add(Dense(units=self.env.allActionsKeys.size,
                        activation="softmax"))

        model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE), metrics=['accuracy'])

        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(state.reshape(-1, state.size))[0]

    def train(self, terminal_state):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get MINIBATCH_SIZE random samples from replay_memory
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Transition: (current_state, action, reward, next_state, done)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_minibatch = self.model.predict(current_states, batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        next_states = np.array([transition[3] for transition in minibatch])
        next_qs_minibatch = self.model.predict(next_states, batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        env_get_legal_actions = self.env.get_legal_actions
        np_max = np.max

        X = []
        y = []

        for index, (current_state, action, reward, next_state, done) in enumerate(minibatch):
            if not done:
                legalActionsIds = env_get_legal_actions(next_state)
                max_next_q = np_max(next_qs_minibatch[index][legalActionsIds])

                new_q = reward + DISCOUNT * max_next_q
            else:
                new_q = reward

            current_qs = current_qs_minibatch[index].copy()
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False)  #, callbacks=[self.tensorboard] if terminal_state else None)
