from Planning_Module.Planner import *
from Encoding_Module_Normalization.environment_Normalization import *
from Learning_Module_Normalization.DeepQLearning_Normalization import *
from Learning_Module.DeepQLearning import *
from Learning_Module_Normalization.DDQNAgent_Normalization import *
from Learning_Module.DDQNAgent import *
import time


if __name__ == '__main__':
    folder3 = "DDQL_2ndEncoding (Min-Max norm.)"
    folder2 = "DDQL_2ndEncoding (NO norm.)"
    # folder3 = "DDQL_2ndEncoding (Z-score norm.)"

    env = EnvironmentNorm()

    for idx in range(3,5):
        agent = DDQNAgent(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg(env, agent, idx, folder2)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder2, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder2}/{PROBLEM}-{idx}.h5")
        solution, score, finished = get_plan_norm(env, agent)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder2}/{idx}")

    for idx in range(3,5):
        agent = DDQNAgentNorm(env)

        start_time = time.time()
        exp_results = deep_q_learning_alg_norm(env, agent, idx, folder3)
        colorPrint(str(time.time() - start_time), YELLOW)

        exp_results.save_data(folder3, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder3}/{PROBLEM}-{idx}.h5")
        solution, score, finished = get_plan_norm(env, agent)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder3}/{idx}")
