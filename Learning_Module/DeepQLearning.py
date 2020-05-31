import time
import os

from hyperparameters_DQL import *
from Encoding_Module.environment import *
# from DQNAgent import *
from DDQNAgent import *


def deep_q_learning_alg():

    np_argmax = np.argmax
    np_append = np.append
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
    ep_lengths = []
    ep_durations = []
    avgScores = np.array([])
    avgLengths = np.array([])
    avgDurations = np.array([])

    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 0
        done = False
        current_state = env_reset()

        start_time = time.time()

        while not done and step < MAX_STEP_PER_EPISODE:
            if np_random_number() > epsilon:  # Take legal action greedily
                actionsQValues = agent_get_qs(current_state)
                legalActionsIds = env_get_legal_actions(current_state)
                # Make the argmax selection among the legal actions
                action = legalActionsIds[np_argmax(actionsQValues[legalActionsIds])]
            else:  # Take random legal action
                action = env_sample()

            new_state, reward, done = env_step(action)

            episode_reward += reward

            agent_update_replay_memory((current_state, action, reward, new_state, done))
            agent_train(done)

            current_state = new_state
            step += 1

        # Append episode reward to a list and log stats (every given number of episodes)
        ep_rewards.append(episode_reward)
        ep_lengths.append(step)
        ep_durations.append(time.time() - start_time)

        if not episode % AGGREGATE_STATS_EVERY:
            average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
            # min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
            # max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])

            average_length = sum(ep_lengths[-AGGREGATE_STATS_EVERY:]) / len(ep_lengths[-AGGREGATE_STATS_EVERY:])
            average_duration = sum(ep_durations[-AGGREGATE_STATS_EVERY:]) / len(ep_durations[-AGGREGATE_STATS_EVERY:])

            avgScores = np_append(avgScores, average_reward)
            avgLengths = np_append(avgLengths, average_length)
            avgDurations = np_append(avgDurations, average_duration if not avgDurations.size else avgDurations[-1] + average_duration)

            print(f"Episode {episode} --> Score: {int(episode_reward)} | Average score: {int(average_reward)} | Epsilon: {epsilon} | Steps: {step}")
            colorPrint(str(average_duration), YELLOW)

            # Save model, but only when min reward is greater or equal a set value
            # if average_reward > GOAL_REWARD + GOAL_REWARD * ((len(env.goal_state) - 1) / len(env.goal_state)):
            #     # Create models folder
            #     if not os.path.isdir('models'):
            #         os.makedirs('models')
            #     agent.model.save(f'models/{MODEL_NAME}__{average_reward}avg__{int(time.time())}.model')
            #     break

        # Decay epsilon
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY

    # Create models folder
    if not os.path.isdir('models'):
        os.makedirs('models')
        agent.model.save(f'models/{MODEL_NAME}__{average_reward}avg__{int(time.time())}.model')

    return avgScores, np.arange(AGGREGATE_STATS_EVERY, avgScores.size * AGGREGATE_STATS_EVERY + AGGREGATE_STATS_EVERY, step=AGGREGATE_STATS_EVERY), avgLengths, avgDurations

def get_plan():
    plan = []

    append = plan.append
    np_argmax = np.argmax

    agent_get_qs = agent.get_qs

    env_reset = env.reset
    env_step = env.step
    env_get_legal_actions = env.get_legal_actions

    episode_reward = 0
    step = 0
    done = False
    current_state = env_reset()

    while not done and step < 10:
        # Take actions greedily
        actionsQValues = agent_get_qs(current_state)
        legalActionsIds = env_get_legal_actions(current_state)
        # Make the argmax selection among the legal actions
        action = legalActionsIds[np_argmax(actionsQValues[legalActionsIds])]

        append(env.allActionsKeys[action])

        new_state, reward, done = env_step(action)

        episode_reward += reward

        current_state = new_state
        step += 1

    return plan, episode_reward, done

if __name__ == '__main__':
    env = Environment()
    # agent = DQNAgent(env)
    agent = DDQNAgent(env)

    avg_scores, episodes, avg_lengths, avg_durations = deep_q_learning_alg()
    solution, score, finished = get_plan()

    print(f"Length of solution: {len(solution)} | Score: {score} | Done: {finished}")
    print(solution)

    generate_graphs(episodes, avg_scores, avg_lengths, avg_durations)
