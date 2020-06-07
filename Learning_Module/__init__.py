from Encoding_Module.environment import *
from DeepQLearning import *
from DQNAgent import *
from DDQNAgent import *
from DDQLAgent_PlanReuse import *
from utils import *
import time


if __name__ == '__main__':
    folder = "DDQL_elevators_p4"
    idx = 0

    # env = Environment()
    env = Environment()

    # agent = DQNAgent(env)
    agent = DDQNAgent(env)
    # agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, REDUCE_ACTION_SPACE))

    start_time = time.time()
    exp_results = deep_q_learning_alg(env, agent, REDUCE_ACTION_SPACE)
    colorPrint(str(time.time() - start_time), YELLOW)

    solution, score, finished = get_plan(env, agent, REDUCE_ACTION_SPACE)

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    exp_results.save_data(folder, idx)
    exp_results.plot_results()