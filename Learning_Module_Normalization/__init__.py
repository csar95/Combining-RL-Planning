from Planning_Module.Planner import *
from Encoding_Module_Normalization.environment_Normalization import *
from DeepQLearning_Normalization import *
from DDQNAgent_Normalization import *
import time


if __name__ == '__main__':
    folder = "_ (wNorm)"
    idx = 0

    env = EnvironmentNorm()
    agent = DDQNAgentNorm(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg_norm(env, agent, idx, folder)
    colorPrint(str(time.time() - start_time), YELLOW)

    exp_results.save_data(folder, idx)
    # exp_results.plot_results()

    planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{folder}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
    solution, score, finished = planner.get_plan()
    planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{folder}/{idx}")
