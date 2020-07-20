from Planning_Module.Planner import *
from Encoding_Module_Non_binary_encoding.environment_Normalization import *
from Learning_Module_Non_binary_encoding.DeepQLearning_Normalization import *
from Learning_Module_Non_binary_encoding.DDQNAgent_Normalization import *
from Learning_Module.DDQNAgent import *

import time


if __name__ == '__main__':
    idx = 99
    folder = "DDQL_Non_binary_encoding"

    env = EnvironmentNorm()

    agent = DDQNAgentNorm(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg_norm(env, agent, idx, folder)
    colorPrint(str(time.time() - start_time), YELLOW)

    exp_results.save_data(folder, idx)

    planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder}/{PROBLEM}-{idx}.h5")
    solution, score, finished = get_plan_norm(env, agent)
    planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder}/{idx}")
