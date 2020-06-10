from Planning_Module.Planner import *

from Encoding_Module.environment import *

from Learning_Module.DeepQLearning import *
from Learning_Module.DQNAgent import *
from Learning_Module.DDQLAgent_PlanReuse import *

from Learning_Module_PER.DDeepQLearningPER import *
from Learning_Module_PER.DDQNAgentPER import *

from Encoding_Module_Normalization.environment_Normalization import *
from Learning_Module_Normalization.DeepQLearning_Normalization import *
from Learning_Module_Normalization.DDQNAgent_Normalization import *


if __name__ == '__main__':
    folder1 = "DDQL_elevators_p4 (RP_1)"
    folder2 = "DQL_elevators_p4"
    folder3 = "DDQL_elevators_p4 (PER)"
    folder4 = "DDQL_elevators_p4 (wNorm)"

    # env = Environment()
    env_norm = EnvironmentNorm()

    # for idx in range(2):
    #     agent = DQNAgent(env)
    #
    #     print(f"------------------------------- {idx} -------------------------------")
    #
    #     exp_results = deep_q_learning_alg(env, agent, idx, folder2)
    #     exp_results.save_data(folder2, idx)
    #
    #     planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{folder2}/{PROBLEM}-{idx}.h5")
    #     solution, score, finished = planner.get_plan()
    #     planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{folder2}/{idx}")

    # for idx in range(2):
    #     agent = DDQNAgentPER(env)
    #
    #     print(f"------------------------------- {idx} -------------------------------")
    #
    #     exp_results = deep_q_learning_alg_per(env, agent)
    #     exp_results.save_data(folder3, idx)

    # for idx in range(2):
    #     agent = DDQNAgentNorm(env_norm)
    #
    #     print(f"------------------------------- {idx} -------------------------------")
    #
    #     exp_results = deep_q_learning_alg_norm(env_norm, agent, idx, folder4)
    #     exp_results.save_data(folder4, idx)
    #
    #     planner = Planner(env_norm, pathtomodel=f"{MODELS_FOLDER}{folder4}/{PROBLEM}-{idx}.h5")
    #     solution, score, finished = planner.get_plan()
    #     planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{folder4}/{idx}")
