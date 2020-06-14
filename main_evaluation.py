from Planning_Module.Planner import *

from Encoding_Module.environment import *
from Encoding_Module_Normalization.environment_Normalization import *

from Learning_Module.DeepQLearning import *
from Learning_Module.DQNAgent import *
from Learning_Module.DDQNAgent import *
from Learning_Module.DDQLAgent_PlanReuse import *

from Learning_Module_PER.DDeepQLearningPER import *
from Learning_Module_PER.DDQNAgentPER import *

from Learning_Module_Normalization.DeepQLearning_Normalization import *
from Learning_Module_Normalization.DDQNAgent_Normalization import *


if __name__ == '__main__':
    # folder1 = "DoubleDQL"
    folder2 = "DDQL_PR_3"
    # folder3 = ""
    # folder4 = ""

    env = Environment()
    # env_norm = EnvironmentNorm()

    # for idx in range(2,3):
    #     agent = DDQNAgent(env)
    #
    #     print(f"------------------------------- {idx} -------------------------------")
    #
    #     exp_results = deep_q_learning_alg(env, agent, idx, folder1)
    #     exp_results.save_data(folder1, idx)
    #
    #     planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder1}/{PROBLEM}-{idx}.h5")
    #     solution, score, finished = get_plan(env, agent)
    #     planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder1}/{idx}")

    env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, reduceactionspace=REDUCE_ACTION_SPACE)

    for idx in range(1,4):
        agent = DDQNAgent(env)

        print(f"------------------------------- {idx} -------------------------------")

        exp_results = deep_q_learning_alg(env, agent, idx, folder2, reduceactionspace=REDUCE_ACTION_SPACE)
        exp_results.save_data(folder2, idx)

        planner = Planner(env, pathtomodel=f"{MODELS_FOLDER}{PROBLEM}/{folder2}/{PROBLEM}-{idx}.h5", reduceactionspace=REDUCE_ACTION_SPACE)
        solution, score, finished = get_plan(env, agent, reduceactionspace=REDUCE_ACTION_SPACE)
        planner.save_plan(solution, pathtodata=f"{DATA_FOLDER}{PROBLEM}/{folder2}/{idx}")
