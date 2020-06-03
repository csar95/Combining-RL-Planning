from Encoding_Module.environment import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DDQNAgent import *

from utils import *


if __name__ == '__main__':
    folder = "DDQL_elevators_p3"

    env = Environment()
    agent = DDQNAgent(env)

    for idx in range(5):
        avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent)

        write_data(episodes, folder, "episodes", idx)
        write_data(avg_scores, folder, "avg_scores", idx)
        write_data(avg_durations, folder, "avg_durations", idx)
        write_data(avg_lengths, folder, "avg_lengths", idx)

        print(f"------------------------------- {idx} -------------------------------")
