from Encoding_Module_Normalization.environment_Normalization import *
from DeepQLearning_Normalization import *
from DQNAgent_Normalization import *
from hyperparameters import *
import time


if __name__ == '__main__':
    folder = ""
    idx = 0

    env = EnvironmentNorm()
    agent = DDQNAgentNorm(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg_norm(env, agent)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan_norm(env, agent)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    exp_results.save_data(folder, idx)
    exp_results.plot_results()