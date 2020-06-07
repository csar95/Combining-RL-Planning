from metrics import *
from hyperparameters import *
import torch as T
import time
import numpy as np


def deep_q_learning_alg(env, agent):
    t_max = T.max
    np_random_number = np.random.random

    agent_get_qs = agent.get_qs
    agent_update_replay_memory = agent.update_replay_memory
    agent_train = agent.train

    env_reset = env.reset
    env_sample = env.sample
    env_step = env.step
    env_get_legal_actions = env.get_legal_actions

    epsilon = 1  # Going to be decayed
    exp_results = Metrics()

    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 1
        done = False
        current_state = env_reset()

        start_time = time.time()

        while not done:
            # TODO: ALTERNATIVE (LAST OPTION) MAKE THE MODEL LEARN ILLEGAL ACTIONS BY GIVING A LARGE NEGATIVE REWARD AND NOT CHANGING THE STATE
            if np_random_number() > epsilon:  # Take legal action greedily
                actionsQValues = agent_get_qs(current_state)
                legalActionsIds = env_get_legal_actions(current_state)
                # Make the argmax selection among the legal actions
                action = legalActionsIds[t_max(actionsQValues[legalActionsIds], dim=0)[1]]
            else:  # Take random legal action
                action = env_sample()

            new_state, reward, done = env_step(action)

            episode_reward += reward

            agent_update_replay_memory((current_state, action, reward, new_state, done))
            agent_train()

            current_state = new_state
            step += 1

        # Append episode reward to a list and log stats (every given number of episodes)
        exp_results.add(episode_score=episode_reward,
                        episode_length=step,
                        episode_duration=time.time() - start_time)

        if episode % SHOW_STATS_EVERY == 0:
            average_reward, average_length, average_duration, _, _ = exp_results.get_average_data(SHOW_STATS_EVERY)
            print(f"Episode {episode} --> Score: {int(episode_reward)} | Avg. Score: {int(average_reward)} | Avg. duration: {average_duration} | Avg. length: {int(average_length)} | Epsilon: {epsilon}")

        # Decay epsilon
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY

    return exp_results

def get_plan(env, agent):
    plan = []

    append = plan.append
    t_max = T.max

    agent_get_qs = agent.get_qs

    env_reset = env.reset
    env_step = env.step
    env_get_legal_actions = env.get_legal_actions

    episode_reward = 0
    step = 1
    done = False
    current_state = env_reset()

    while not done and step < 10:
        # Take actions greedily
        actionsQValues = agent_get_qs(current_state)
        legalActionsIds = env_get_legal_actions(current_state)
        # Make the argmax selection among the legal actions

        _, idx = t_max(actionsQValues[legalActionsIds], dim=0)
        action = legalActionsIds[idx]

        append(env.allActionsKeys[action])

        new_state, reward, done = env_step(action)

        episode_reward += reward

        current_state = new_state
        step += 1

    return plan, episode_reward, done
