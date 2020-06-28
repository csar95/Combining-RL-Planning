from Planning_Module.Planner import *
from Encoding_Module.environment import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DQNAgent import *
from Learning_Module.DDQNAgent import *
from Learning_Module.DDQLAgent_PlanReuse import *
from utils import *
from hyperparameters import *

import time


if __name__ == '__main__':
    # folder1 = "DDQL_PR_2 (20000)"
    # folder2 = "DDQL_PR_1 (0.8)"
    folder3 = "DoubleDQL"

    env = Environment()
    # env.get_previous_plans(reduceactionspace=True)  # True ==> 3rd & 6th approaches

    # for idx in range(3):
    #
    #     # agent = DQNAgent(env)
    #     # agent = DDQNAgent(env)
    #     agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(reduceactionspace=REDUCE_ACTION_SPACE), allexpmixed=True)
    #
    #     start_time = time.time()
    #     exp_results = deep_q_learning_alg(env, agent, idx, folder1)
    #     colorPrint(str(time.time() - start_time), YELLOW)
    #
    #     exp_results.save_data(folder1, idx)
    #
    #     planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder1}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)  # True ==> 3rd approach | False ==> 6th approach
    #     solution, score, finished = get_plan(env, agent, reduceactionspace=REDUCE_ACTION_SPACE)  # True ==> 3rd approach | False ==> 6th approach
    #     planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder1}/{idx}")

    # for idx in range(2):
    #     # agent = DQNAgent(env)
    #     # agent = DDQNAgent(env)
    #     agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(reduceactionspace=REDUCE_ACTION_SPACE), allexpmixed=False)
    #
    #     start_time = time.time()
    #     exp_results = deep_q_learning_alg(env, agent, idx, folder2)
    #     colorPrint(str(time.time() - start_time), YELLOW)
    #
    #     exp_results.save_data(folder2, idx)
    #
    #     planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder2}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)  #  True ==> 3rd approach | False ==> 6th approach
    #     solution, score, finished = get_plan(env, agent, reduceactionspace=REDUCE_ACTION_SPACE)  #  True ==> 3rd approach | False ==> 6th approach
    #     planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder2}/{idx}")

    for idx in range(2,5):
        agent = DDQNAgent(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg(env, agent, idx, folder3)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder3, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder3}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)  #  True ==> 3rd approach | False ==> 6th approach
        solution, score, finished = get_plan(env, agent, reduceactionspace=REDUCE_ACTION_SPACE)  #  True ==> 3rd approach | False ==> 6th approach
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder3}/{idx}")
