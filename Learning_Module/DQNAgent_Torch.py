import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque
import random
import numpy as np

from hyperparameters_DQL import *


class DeepQNetwork(nn.Module ):

    def __init__(self, env):
        super(DeepQNetwork, self).__init__()

        self.env = env

        self.hiddenLayer1Nodes = 32

        self.hiddenLayer1 = nn.Linear(in_features=self.env.state.size, out_features=self.hiddenLayer1Nodes)
        self.outputLayer = nn.Linear(in_features=self.hiddenLayer1Nodes, out_features=self.env.allActionsKeys.size)

        self.optimizer = optim.Adam(self.parameters(), lr=LEARNING_RATE)
        self.loss = nn.MSELoss()

class DQL_Agent:

    def __init__(self, env):
        self.env = env

        self.model = DeepQNetwork(env)

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

    def get_qs(self, state):
        x = F.relu(input=self.model.hiddenLayer1(T.Tensor(state)))
        return F.softmax(input=self.model.outputLayer(x), dim=0)

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def train(self):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        self.model.optimizer.zero_grad()

        #  Get MINIBATCH_SIZE random samples from replay_memory
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_minibatch = self.get_qs(current_states)
        target_qs_minibatch = current_qs_minibatch.clone()

        next_states = np.array([transition[3] for transition in minibatch])
        next_qs_minibatch = self.get_qs(next_states)

        env_get_legal_actions = self.env.get_legal_actions
        t_max = T.max

        for index, (current_state, action, reward, next_state, done) in enumerate(minibatch):
            if not done:
                legalActionsIds = env_get_legal_actions(next_state)
                max_next_q = t_max(next_qs_minibatch[index][legalActionsIds])

                new_q = reward + DISCOUNT * max_next_q
            else:
                new_q = reward

            target_qs_minibatch[index][action] = new_q

        loss = self.model.loss(target_qs_minibatch, current_qs_minibatch)
        loss.backward()
        self.model.optimizer.step()
