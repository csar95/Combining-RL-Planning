from Encoding_Module.environment import *
from DDeepQLearningPER import *
from DDQNAgentPER import *
import time


if __name__ == '__main__':
    env = Environment()
    agent = DDQNAgentPER(env)

    start_time = time.time()
    scores, lengths, durations = deep_q_learning_alg(env, agent)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    episodes, avg_scores, avg_lengths, avg_durations = get_average_data_to_plot(scores, lengths, durations)
    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)
