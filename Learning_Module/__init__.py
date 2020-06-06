from Encoding_Module.environment import *
from DeepQLearning import *
from DQNAgent import *
from DDQNAgent import *
from DDQLAgent_PlanReuse import *
from utils import *
import time


if __name__ == '__main__':
    folder = ""
    idx = 0

    # env = Environment()
    env = Environment()

    # agent = DQNAgent(env)
    agent = DDQNAgent(env)
    # agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, REDUCE_ACTION_SPACE))

    start_time = time.time()
    scores, lengths, durations = deep_q_learning_alg(env, agent, REDUCE_ACTION_SPACE)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan(env, agent, REDUCE_ACTION_SPACE)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    write_data(scores, folder, "scores", idx)
    write_data(lengths, folder, "lengths", idx)
    write_data(durations, folder, "durations", idx)

    episodes, avg_scores, avg_lengths, avg_durations = get_average_data_to_plot(scores, lengths, durations)
    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)