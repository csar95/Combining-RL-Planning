from Planning_Module.Planner import *
from Encoding_Module.environment import *
from DDeepQLearningPER import *
from DDQNAgentPER import *
import time


if __name__ == '__main__':
    folder3 = "DDQL_PER_0.1"
    folder1 = "DDQL_PER_0.7"
    folder2 = "DDQL_PER_0.9"

    env = Environment()

    for idx in range(5):
        agent = DDQNAgentPER(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder3, a=0.1)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder3, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder3}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
        solution, score, finished = get_plan_per(env, agent)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder3}/{idx}")

    for idx in range(5):
        agent = DDQNAgentPER(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder1, a=0.7)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder1, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder1}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
        solution, score, finished = get_plan_per(env, agent)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder1}/{idx}")

    for idx in range(5):
        agent = DDQNAgentPER(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg_per(env, agent, idx, folder2, a=0.9)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder2, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder2}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
        solution, score, finished = get_plan_per(env, agent)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder2}/{idx}")
