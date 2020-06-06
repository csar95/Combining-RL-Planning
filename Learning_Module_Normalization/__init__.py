from Encoding_Module_Normalization.environment_Normalization import *
from DeepQLearning_Normalization import *
from DQNAgent_Normalization import *
import time


if __name__ == '__main__':
    env = EnvironmentNorm()
    agent = DDQNAgentNorm(env)

    start_time = time.time()
    scores, lengths, durations = deep_q_learning_alg_norm(env, agent)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan_norm(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    episodes, avg_scores, avg_lengths, avg_durations = get_average_data_to_plot(scores, lengths, durations)
    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)
