import time
import os
import numpy as np
from hyperparameters_DQL import *
import torch as T


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
    ep_rewards = []

    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 1
        done = False
        current_state = env_reset()

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
        ep_rewards.append(episode_reward)

        if not episode % AGGREGATE_STATS_EVERY:
            average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
            # min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
            # max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])

            print(f"Episode {episode} --> Score: {episode_reward} | Average score: {average_reward} | Epsilon: {epsilon}")

            # Save model, but only when min reward is greater or equal a set value
            if average_reward >= GOAL_REWARD:
                # Create models folder
                if not os.path.isdir('models'):
                    os.makedirs('models')
                agent.model.save(f'models/{MODEL_NAME}__{average_reward}avg__{int(time.time())}.model')
                # agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')
                break

        # Decay epsilon
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            # epsilon = max(MIN_EPSILON, epsilon)

    return np.array(ep_rewards), np.arange(1, episode+1)

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
