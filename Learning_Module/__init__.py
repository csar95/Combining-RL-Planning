from Encoding_Module.environment import *
from DeepQLearning import *
from DQNAgent import *
from DDQNAgent import *


if __name__ == '__main__':
    env = Environment()
    # agent = DQNAgent(env)
    agent = DDQNAgent(env)

    avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg(env, agent)
    solution, score, finished = get_plan(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)