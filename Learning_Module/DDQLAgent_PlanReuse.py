from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.metrics import Precision, Recall
from collections import deque
import random
from utils import *
from hyperparameters import *


class ReplayBuffer:
    def __init__(self, prevexp, maxlen, allexpmixed):
        self.allExpMixed = allexpmixed
        self.previousExperiences = prevexp
        self.localBuffer = deque(maxlen=(maxlen - len(self.previousExperiences)) if self.allExpMixed else maxlen)

    def add(self, experience):
        self.localBuffer.append(experience)

    def sample(self, batch_size):
        if self.allExpMixed:
            return random.sample(list(self.localBuffer) + self.previousExperiences, k=batch_size)
        else:
            samples = random.sample(self.previousExperiences, k=int(batch_size * REUSE_RATE))
            samples.extend(random.sample(self.localBuffer, k=int(batch_size * (1 - REUSE_RATE))))
            return samples

class DDQLAgent_PlanReuse:

    def __init__(self, env, prevexp, allexpmixed):
        self.env = env

        # Main model. The one that gets trained every step
        self.model = self.create_model()

        self.targetModel = self.create_model()
        self.targetModel.set_weights(self.model.get_weights())
        self.targetUpdateCounter = 0

        self.replay_memory = ReplayBuffer(prevexp, maxlen=REPLAY_MEMORY_SIZE, allexpmixed=allexpmixed)

    def create_model(self):
        model = Sequential()

        hiddenLayerSize = 0
        for i in range(20):
            if 2**i > self.env.allActionsKeys.size:
                hiddenLayerSize = 2**i
                break

        model.add(Dense(units=hiddenLayerSize,
                        activation="relu",
                        input_dim=self.env.state.size)),
        model.add(Dense(units=self.env.allActionsKeys.size,
                        activation="linear"))

        model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE), metrics=[Recall(name="recall"), Precision(name="precision")])

        return model

    def update_replay_memory(self, transition):
        self.replay_memory.add(transition)
        self.targetUpdateCounter += 1

    def get_qs(self, state):
        return self.model.predict(state.reshape(-1, state.size))[0]

    def train(self, reduceactionspace=False):
        if len(self.replay_memory.localBuffer) < MIN_REPLAY_MEMORY_SIZE * (1 - REUSE_RATE):
            return -1, -1, -1

        # Get MINIBATCH_SIZE random samples from replay_memory
        minibatch = self.replay_memory.sample(MINIBATCH_SIZE)

        # Transition: (current_state, action, reward, next_state, done)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_minibatch = self.model.predict(current_states, batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        next_states = np.array([transition[3] for transition in minibatch])
        next_qs_eval_minibatch = self.model.predict(next_states, batch_size=MINIBATCH_SIZE, use_multiprocessing=True)
        next_qs_target_minibatch = self.targetModel.predict(next_states, batch_size=MINIBATCH_SIZE, use_multiprocessing=True)

        env_get_legal_actions = self.env.get_legal_actions
        np_argmax = np.argmax

        X = []
        y = []

        for index, (current_state, action, reward, next_state, done) in enumerate(minibatch):
            if not done:
                legalActionsIds = env_get_legal_actions(next_state, reduceactionspace)
                maxAction = legalActionsIds[ np_argmax(next_qs_eval_minibatch[index][legalActionsIds]) ]
                max_next_q = next_qs_target_minibatch[index][maxAction]

                new_q = reward + DISCOUNT * max_next_q
            else:
                new_q = reward

            current_state_target_qs = current_qs_minibatch[index].copy()
            current_state_target_qs[action] = new_q

            X.append(current_state)
            y.append(current_state_target_qs)

        history = self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False).history

        # Update the target model periodically based on the local model
        if HARD_UPDATE and self.targetUpdateCounter % UPDATE_TARGET_EVERY == 0:
            self.hard_update_target_model()
        elif not HARD_UPDATE:
            self.soft_update_target_model()

        return history['loss'][0], history['recall'][0], history['precision'][0]

    def hard_update_target_model(self):
        self.targetModel.set_weights(self.model.get_weights())

    def soft_update_target_model(self):
        q_model_theta = self.model.get_weights()
        target_model_theta = self.targetModel.get_weights()

        for idx, (q_weight, target_weight) in enumerate(zip(q_model_theta, target_model_theta)):
            target_weight = target_weight * (1 - TAU) + q_weight * TAU
            target_model_theta[idx] = target_weight

        self.targetModel.set_weights(target_model_theta)
