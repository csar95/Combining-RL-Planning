from Encoding_Module.environment import *
from DDeepQLearningPER import *
from DDQNAgentPER import *
import time


if __name__ == '__main__':
    folder1 = "DDQL_PER_0.7"
    folder2 = "DDQL_PER_0.9"
    folder3 = "DDQL_PER_0.1"

    env = Environment()

    for idx in range(3):
        agent = DDQNAgentPER(env)

        print(f"------------------------------- {idx} -------------------------------")

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder1, a=0.7)
        colorPrint(str(time.time() - start_time), YELLOW)

        solution, score, finished = get_plan_per(env, agent)

        print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
        print(solution)

        exp_results.save_data(folder1, idx)

    for idx in range(3):
        agent = DDQNAgentPER(env)

        print(f"------------------------------- {idx} -------------------------------")

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder2, a=0.9)
        colorPrint(str(time.time() - start_time), YELLOW)

        solution, score, finished = get_plan_per(env, agent)

        print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
        print(solution)

        exp_results.save_data(folder2, idx)

    for idx in range(3):
        agent = DDQNAgentPER(env)

        print(f"------------------------------- {idx} -------------------------------")

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder3, a=0.1)
        colorPrint(str(time.time() - start_time), YELLOW)

        solution, score, finished = get_plan_per(env, agent)

        print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
        print(solution)

        exp_results.save_data(folder3, idx)