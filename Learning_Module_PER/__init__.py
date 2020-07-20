from Planning_Module.Planner import *
from Encoding_Module.environment import *
from Learning_Module_PER.DDeepQLearningPER import *
from Learning_Module_PER.DDQNAgentPER import *
import time


if __name__ == '__main__':
    idx = 99
    folder = "DDQL_PER"

    env = Environment()

    agent = DDQNAgentPER(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg_per(env, agent, idx, folder, a=ALPHA_PER)
    colorPrint(str(time.time() - start_time), YELLOW)

    exp_results.save_data(folder, idx)

    planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
    solution, score, finished = get_plan_per(env, agent)
    planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder}/{idx}")
