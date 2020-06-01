from Encoding_Module.environment import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DQNAgent import *
from Learning_Module.DDQNAgent import *

from plot import *


if __name__ == '__main__':

    env = Environment()

    agent = DQNAgent(env)
    agent_double = DDQNAgent(env)

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []

    for i in range(5):
        avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent)
        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        print(f"------------------------------ STANDARD DQL {i} ------------------------------")

    for i in range(5):
        avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent_double)
        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        print(f"------------------------------- DOUBLE DQL {i} -------------------------------")

    generate_plots(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set)


