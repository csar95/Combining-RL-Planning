from Encoding_Module.environment import *
from Learning_Module_PER.DDeepQLearningPER import *
from Learning_Module_PER.DDQNAgentPER import *

# from plot import *
from utils import *


if __name__ == '__main__':
    folder = "DoubleDQL_PER"

    env = Environment()
    agent = DDQNAgentPER(env)

    for idx in range(5):
        avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent)

        write_data(episodes, folder, "episodes", idx)
        write_data(avg_scores, folder, "avg_scores", idx)
        write_data(avg_durations, folder, "avg_durations", idx)
        write_data(avg_lengths, folder, "avg_lengths", idx)

        print(f"------------------------------- DOUBLE DQL PER {idx} -------------------------------")
