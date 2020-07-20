from metrics import *
from hyperparameters import *

import time
import numpy as np
import os
from os.path import join


def deep_q_learning_alg(env, agent, idx, folder, initialeta=INITIAL_ETA, mineta=MIN_ETA, etadecay=ETA_DECAY, directory=None, problemfilename=None):
    np_argmax = np.argmax
    np_random_number = np.random.random

    agent_get_qs = agent.get_qs
    agent_update_replay_memory = agent.update_replay_memory
    agent_train = agent.train

    env_reset = env.reset
    env_sample = env.sample
    env_step = env.step
    env_get_legal_actions = env.get_legal_actions

    epsilon = 1  # Going to be decayed
    eta = initialeta
    exp_results = Metrics()

    for episode in range(1, EPISODES+1):
        ep_loss = []
        ep_fscore = []

        episode_reward = 0
        step = 0
        done = False
        current_state = env_reset()

        start_time = time.time()

        while not done and step < MAX_STEP_PER_EPISODE:
            reduceactionspace = np_random_number() < eta  # True ==> Use simplified actions space | False ==> Use full action space

            if np_random_number() > epsilon:  # Take legal action greedily (Exploitation)
                actionsQValues = agent_get_qs(current_state)
                legalActionsIds = env_get_legal_actions(current_state, reduceactionspace)
                # Make the argmax selection among the legal actions
                action = legalActionsIds[np_argmax(actionsQValues[legalActionsIds])]
            else:  # Take random legal action (Exploration)
                action = env_sample(reduceactionspace)

            new_state, reward, done = env_step(action)

            episode_reward += reward

            agent_update_replay_memory((current_state, action, reward, new_state, done))

            loss, recall, precision = agent_train(reduceactionspace)

            if loss != -1:
                ep_loss.append(loss)
                ep_fscore.append(2 * ((precision * recall) / (precision + recall)))

            current_state = new_state
            step += 1

        # Append episode reward to a list and log stats (every given number of episodes)
        exp_results.add(episode_score=episode_reward,
                        episode_length=step,
                        episode_duration=time.time() - start_time,
                        episode_avgLoss=sum(ep_loss) / len(ep_loss) if ep_loss else 0.0,
                        episode_avgFScore=sum(ep_fscore) / len(ep_fscore) if ep_fscore else 0.0)

        if episode % SHOW_STATS_EVERY == 0:
            average_reward, average_length, average_duration, average_loss, average_fscore = exp_results.get_average_data(SHOW_STATS_EVERY)
            print(f"Episode {episode} --> Score: {int(episode_reward)} | Avg. Score: {int(average_reward)} | Avg. Loss: {average_loss} | Avg. F-score: {average_fscore} | Avg. duration: {average_duration} | Avg. length: {int(average_length)} | Epsilon: {epsilon} | Eta: {eta}")

        # Decay epsilon
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY

        # Decay eta
        if eta > mineta:
            eta *= etadecay

    # Create models folder
    pathtomodel = f"{MODELS_FOLDER}{PROBLEM}/{folder}" if not directory else directory
    if not os.path.isdir(pathtomodel):
        os.makedirs(pathtomodel)
    if not directory:
        agent.model.save_weights(f'{pathtomodel}/{PROBLEM}-{idx}.h5')
    else:
        agent.model.save_weights(join(pathtomodel, f"{problemfilename}.h5"))

    return exp_results

def get_plan(env, agent, reduceactionspace=False):
    plan = []

    episode_reward = 0
    step = 0
    done = False
    current_state = env.reset()

    while not done and step < MAX_STEPS_PLANNER:
        # Take actions greedily
        actionsQValues = agent.get_qs(current_state)
        legalActionsIds = env.get_legal_actions(current_state, reduceactionspace)
        # Make the argmax selection among the legal actions
        action = legalActionsIds[np.argmax(actionsQValues[legalActionsIds])]

        plan.append(env.allActionsKeys[action])
        new_state, reward, done = env.step(action)

        episode_reward += reward

        current_state = new_state
        step += 1

    return plan, episode_reward, done