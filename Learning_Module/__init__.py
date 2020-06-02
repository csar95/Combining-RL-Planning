from Encoding_Module.environment import *
from DeepQLearning import *
from DQNAgent import *
from DDQNAgent import *
from utils import *


if __name__ == '__main__':
    folder = "DDQL_elevators_p2"
    idx = 0

    env = Environment()
    # agent = DQNAgent(env)
    agent = DDQNAgent(env)

    avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent)
    solution, score, finished = get_plan(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    write_data(episodes, folder, "episodes", idx)
    write_data(avg_scores, folder, "avg_scores", idx)
    write_data(avg_durations, folder, "avg_durations", idx)
    write_data(avg_lengths, folder, "avg_lengths", idx)

    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)