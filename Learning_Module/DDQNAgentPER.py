from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Activation
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import keras.backend as K
from collections import deque
import time
import random
import numpy as np

from hyperparameters_DQL import *
from utils import *


def custom_MSE(qValues_target, qValues_pred, importance):
        return K.mean(K.square(qValues_pred - qValues_target) * importance, axis=-1)


class PrioritizedReplayBuffer:
    def __init__(self, maxlen):
        self.buffer = deque(maxlen=maxlen)
        self.priorities = deque(maxlen=maxlen)

    def add(self, experience):
        self.buffer.append(experience)
        self.priorities.append(max(self.priorities, default=1))

    def sample(self, batch_size, priority_scale=1.0):
        sample_probs = self.get_probabilities(priority_scale)

        sample_indices = random.choices(range(len(self.buffer)), k=batch_size, weights=sample_probs)

        samples = np.array(self.buffer)[sample_indices]
        importance = self.get_importance(sample_probs[sample_indices])

        return list(samples), importance, sample_indices

    def get_probabilities(self, priority_scale):
        scaled_priorities = np.array(self.priorities) ** priority_scale
        sample_probabilities = scaled_priorities / sum(scaled_priorities)
        return sample_probabilities

    def get_importance(self, probabilities):
        importance = (1/len(self.buffer)) * (1/probabilities)
        importance_normalized = importance / max(importance)
        return importance_normalized

    def set_priorities(self, indices, errors, offset=0.1):
        for i,e in zip(indices, errors):
            self.priorities[i] = abs(e) + offset

class DDQNAgentPER:

    def __init__(self, env):
        self.env = env

        # Main model. The one that gets trained every step
        self.model = self.create_model()

        self.targetModel = self.create_model()
        self.targetModel.set_weights(self.model.get_weights())
        self.targetUpdateCounter = 0

        self.replay_memory = PrioritizedReplayBuffer(maxlen=REPLAY_MEMORY_SIZE)

    def create_model(self):
        hiddenLayerSize = 0
        for i in range(20):
            if 2**i > self.env.allActionsKeys.size:
                hiddenLayerSize = 2**i
                break

        state_in = Input(shape=(self.env.state.size,), name='state_in')
        qValues_target = Input(shape=(self.env.allActionsKeys.size,), name='y_true')
        importance_in = Input(shape=(1,), name='importance_in')
        hiddenLayer = Dense(units=hiddenLayerSize, activation="relu")(state_in)
        qValues_pred = Dense(self.env.allActionsKeys.size, activation='softmax', name='y_pred')(hiddenLayer)

        model = Model(inputs=[state_in, qValues_target, importance_in], outputs=qValues_pred, name='train_only')

        model.add_loss(custom_MSE(qValues_target, qValues_pred, importance_in))
        model.compile(loss=None, optimizer=Adam(lr=LEARNING_RATE), metrics=['accuracy'])

        return model

    def update_replay_memory(self, transition):
        self.replay_memory.add(transition)

    def get_qs(self, state):
        return self.model.predict([state.reshape(-1, state.size),
                                   np.empty(shape=self.env.allActionsKeys.size).reshape(-1, self.env.allActionsKeys.size),
                                   np.empty(shape=self.env.allActionsKeys.size).reshape(-1, 1)])[0]

    def train(self, terminal_state, epsilon, a=0.0):
        if len(self.replay_memory.buffer) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get MINIBATCH_SIZE random samples from replay_memory
        minibatch, importance, indices = self.replay_memory.sample(batch_size=MINIBATCH_SIZE, priority_scale=a)

        empty_qValues_target = np.empty(shape=(MINIBATCH_SIZE, self.env.allActionsKeys.size))
        empty_importance_in = np.empty(shape=(MINIBATCH_SIZE, 1))

        # Transition: (current_state, action, reward, next_state, done)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_minibatch = self.model.predict([current_states, empty_qValues_target, empty_importance_in], batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        next_states = np.array([transition[3] for transition in minibatch])
        next_qs_eval_minibatch = self.model.predict([next_states, empty_qValues_target, empty_importance_in], batch_size=MINIBATCH_SIZE, use_multiprocessing=True)
        next_qs_target_minibatch = self.targetModel.predict([next_states, empty_qValues_target, empty_importance_in], batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        env_get_legal_actions = self.env.get_legal_actions
        np_argmax = np.argmax

        X = []
        y = []
        errors = []

        for index, (current_state, action, reward, next_state, done) in enumerate(minibatch):
            if not done:
                legalActionsIds = env_get_legal_actions(next_state)
                maxAction = legalActionsIds[ np_argmax(next_qs_eval_minibatch[index][legalActionsIds]) ]
                max_next_q = next_qs_target_minibatch[index][maxAction]

                new_q = reward + DISCOUNT * max_next_q
            else:
                new_q = reward

            errors.append(current_qs_minibatch[index][action] - new_q)

            current_state_target_qs = current_qs_minibatch[index].copy()
            current_state_target_qs[action] = new_q

            X.append(current_state)
            y.append(current_state_target_qs)

        self.model.fit([np.array(X), np.array(y), importance ** (1-epsilon)], batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False)

        self.replay_memory.set_priorities(indices, errors)

        if terminal_state:
            self.targetUpdateCounter += 1

        # Update the target model periodically based on the local model
        if self.targetUpdateCounter % UPDATE_TARGET_EVERY == 0:
            self.targetModel.set_weights(self.model.get_weights())
