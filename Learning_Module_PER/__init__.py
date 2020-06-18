from Encoding_Module.environment import *
from DDeepQLearningPER import *
from DDQNAgentPER import *
import time


if __name__ == '__main__':
    folder = "DDQL_PER"

    env = Environment()

    for idx in range(3):
        agent = DDQNAgentPER(env)

        print(f"------------------------------- {idx} -------------------------------")

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder)
        colorPrint(str(time.time() - start_time), YELLOW)

        solution, score, finished = get_plan_per(env, agent)

        print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
        print(solution)

        exp_results.save_data(folder, idx)
        # exp_results.plot_results()