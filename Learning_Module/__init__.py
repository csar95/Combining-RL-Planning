from Planning_Module.Planner import *
from Encoding_Module.environment import *
from DeepQLearning import *
from DQNAgent import *
from DDQNAgent import *
from DDQLAgent_PlanReuse import *
from utils import *
import time


if __name__ == '__main__':
    folder = "DDQL_elevators_p4 (RP_3)"
    idx = 4

    # env = Environment()
    env = Environment()
    env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, reduceactionspace=REDUCE_ACTION_SPACE)

    # agent = DQNAgent(env)
    agent = DDQNAgent(env)
    # agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, reduceactionspace=REDUCE_ACTION_SPACE), allexpmixed=True)

    start_time = time.time()
    exp_results = deep_q_learning_alg(env, agent, idx, folder, REDUCE_ACTION_SPACE)
    colorPrint(str(time.time() - start_time), YELLOW)

    exp_results.save_data(folder, idx)
    # exp_results.plot_results()

    planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{folder}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
    solution, score, finished = planner.get_plan()
    planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{folder}/{idx}")
