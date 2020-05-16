from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import time
import random
import os
import numpy as np

from hyperparameters_DQL import *


# Create models folder
if not os.path.isdir('models'):
    os.makedirs('models')


class DQNAgent:

    def __init__(self, env):
        self.env = env

        # Main model. The one that gets trained every step
        self.model = self.create_model()

        # Target model. The one we .predict against every step
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())
        self.target_update_counter = 0

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        self.tensorboard = TensorBoard(log_dir=f"log/{MODEL_NAME}-{int(time.time())}")

    def create_model(self):
        model = Sequential()

        model.add(Dense(units=int(self.env.state.size+((self.env.allActionsKeys.size-self.env.state.size)/2)),
                        activation="relu",
                        input_shape=(self.env.state.size,)))
        model.add(Dense(units=self.env.allActionsKeys.size,
                        activation="softmax"))

        model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE), metrics=['accuracy'])

        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(state.reshape(-1, *state.shape))[0]

    def train(self, terminal_state):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get MINIBATCH_SIZE random samples from replay_memory
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Transition: (current_state, action, reward, new_current_state, done)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        env_get_legal_actions = self.env.get_legal_actions
        np_max = np.max

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                legalActionsIds = env_get_legal_actions(new_current_state)
                max_future_q = np_max(future_qs_list[index][legalActionsIds])

                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False)  #, callbacks=[self.tensorboard] if terminal_state else None)

        # Updating to determine if we want to update target_model yet
        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
