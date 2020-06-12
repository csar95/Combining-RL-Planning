from Planning_Module.Planner import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DDQNAgent import *
from Encoding_Module.environment import *


if __name__ == '__main__':

    folder = "DoubleDQL"
    idx = 0

    env = Environment()
    agent = DDQNAgent(env)

    start_time = time.time()
    exp_results = deep_q_learning_alg(env, agent, idx, folder, REDUCE_ACTION_SPACE)
    colorPrint(str(time.time() - start_time), YELLOW)

    exp_results.save_data(folder, idx)
    # exp_results.plot_results()

    planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
    plan, score, finished = planner.get_plan()
    planner.save_plan(plan, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder}/{idx}")
