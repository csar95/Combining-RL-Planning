from Encoding_Module.environment import *
from Learning_Module.DeepQLearning import *
from Learning_Module.DDQNAgent import *


if __name__ == '__main__':
    folder1 = "DDQL_elevators_p4"
    folder2 = "DDQL_elevators_p4 (Prev. Plans)"

    env = Environment()

    # for idx in range(1,3):
    #     agent = DDQNAgent(env)
    #
    #     print(f"------------------------------- {idx} -------------------------------")
    #
    #     exp_results = deep_q_learning_alg(env, agent, False)
    #     exp_results.save_data(folder1, idx)

    for idx in [0, 3]:
        env.get_previous_plans(NUMBER_OF_PREVIOUS_PLANS, True)
        agent = DDQNAgent(env)

        print(f"------------------------------- {idx} -------------------------------")

        exp_results = deep_q_learning_alg(env, agent, True)
        exp_results.save_data(folder2, idx)
