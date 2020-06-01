import matplotlib.pyplot as plt
import numpy as np
import re
from utils import *


path = "StandardDQLvsDoubleDQL"

def generate_plots(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set):
    plt.figure(figsize=(8, 6))

    plt.xlim([0, max([np.max(episodes) for episodes in episodes_set])])
    plt.xlabel('Episode')
    plt.ylabel('Average episode score')
    plt.title('Episode reward over time')

    for idx, episodes in enumerate(episodes_set):
        # write_episodes(episodes, idx, path)
        # write_avg_scores(avg_scores_set[idx], idx, path)
        plt.plot(episodes, avg_scores_set[idx], color="firebrick" if idx < 5 else "dodgerblue", linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label="Standard DQL")
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label="Double DQL")
    plt.legend(loc="lower right")
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Comparison_DQLvsDDQL/Learning curve.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, max([np.max(avg_durations) for avg_durations in avg_durations_set])])
    plt.xlabel('Time step')
    plt.ylabel('Episode')
    plt.title('Episode per time step')

    for idx, avg_durations in enumerate(avg_durations_set):
        # write_avg_durations(avg_durations_set[idx], idx, path)
        plt.plot(avg_durations, episodes_set[idx], color='firebrick' if idx < 5 else 'dodgerblue', linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label="Standard DQL")
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label="Double DQL")
    plt.legend(loc="lower right")
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Comparison_DQLvsDDQL/Episodes duration.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, max([np.max(episodes) for episodes in episodes_set])])
    plt.xlabel('Episode')
    plt.ylabel('Average episode length')
    plt.title('Episode length over time')

    for idx, episodes in enumerate(episodes_set):
        # write_avg_lengths(avg_lengths_set[idx], idx, path)
        plt.plot(episodes, avg_lengths_set[idx], color='firebrick' if idx < 5 else 'dodgerblue', linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label="Standard DQL")
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label="Double DQL")
    plt.legend(loc="upper right")
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Comparison_DQLvsDDQL/Episodes length.png')


episodes_set = []
avg_scores_set = []
avg_lengths_set = []
avg_durations_set = []

for i in range(10):
    f = open(f"{path}/episodes-{i}", 'r')
    aux = f.readline().split(',')
    f.close()
    episodes = np.array([float(re.sub('[\[\]]', '', e)) for e in aux])

    f = open(f"{path}/avg_scores-{i}", 'r')
    aux = f.readline().split(',')
    f.close()
    avg_scores = np.array([float(re.sub('[\[\]]', '', e)) for e in aux])

    f = open(f"{path}/avg_lengths-{i}", 'r')
    aux = f.readline().split(',')
    f.close()
    avg_lengths = np.array([float(re.sub('[\[\]]', '', e)) for e in aux])

    f = open(f"{path}/avg_durations-{i}", 'r')
    aux = f.readline().split(',')
    f.close()
    avg_durations = np.array([float(re.sub('[\[\]]', '', e)) for e in aux])

    episodes_set.append(episodes[:160])
    avg_scores_set.append(avg_scores[:160])
    avg_lengths_set.append(avg_lengths[:160])
    avg_durations_set.append(avg_durations[:160])

generate_plots(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set)