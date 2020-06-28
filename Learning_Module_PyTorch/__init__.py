from Encoding_Module.environment import *
from DeepQLearning_Torch import *
from DQNAgent_Torch import *
from utils import *
import time


if __name__ == '__main__':
    folder = "DDQL_elevators_p4"
    idx = 0

    env = Environment()
    agent = DQL_Agent(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg(env, agent)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    exp_results.save_data(folder, idx)
