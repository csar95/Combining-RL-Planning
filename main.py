from Encoding_Module.environment import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DDQNAgent import *

from utils import *


if __name__ == '__main__':
    folder = ""

    env = Environment()
    agent = DDQNAgent(env)

    for idx in range(5):
        scores, lengths, durations = deep_q_learning_alg(env, agent, REDUCE_ACTION_SPACE)

        write_data(scores, folder, "scores", idx)
        write_data(lengths, folder, "lengths", idx)
        write_data(durations, folder, "durations", idx)

        print(f"------------------------------- {idx} -------------------------------")
