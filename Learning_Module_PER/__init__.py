from Encoding_Module.environment import *
from DDeepQLearningPER import *
from DDQNAgentPER import *
import time


if __name__ == '__main__':
    folder = ""
    idx = 0

    env = Environment()
    agent = DDQNAgentPER(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg_per(env, agent)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    exp_results.save_data(folder, idx)
    exp_results.plot_results()