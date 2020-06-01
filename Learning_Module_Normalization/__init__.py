from Encoding_Module_Normalization.environment_Normalization import *
from DeepQLearning_Normalization import *
from DQNAgent_Normalization import *


if __name__ == '__main__':
    env = EnvironmentNorm()
    agent = DDQNAgentNorm(env)

    avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg_norm(env, agent)
    solution, score, finished = get_plan_norm(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)
