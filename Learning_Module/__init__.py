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
    folder = "DDQL_PR_6"

    env = Environment()
    env.get_previous_plans(reduceactionspace=True)  # True ==> 3rd & 6th approaches

    for idx in range(3):

        # agent = DQNAgent(env)
        agent = DDQNAgent(env)
        # agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(reduceactionspace=REDUCE_ACTION_SPACE), allexpmixed=True)

        start_time = time.time()
        exp_results = deep_q_learning_alg(env, agent, idx, folder)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder}/{PROBLEM}-{idx}.h5", reduceactionspace=False)  # True ==> 3rd approach | False ==> 6th approach
        solution, score, finished = get_plan(env, agent, reduceactionspace=False)  # True ==> 3rd approach | False ==> 6th approach
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder}/{idx}")
