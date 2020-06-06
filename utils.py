import matplotlib.pyplot as plt
import numpy as np
import re
from hyperparameters import *


RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
GREY = "\x1b[90m"
RESET = "\x1b[0m"

valid = {
    "yes": True,
    "y": True,
    "no": False,
    "n": False
}

def colorPrint(msg, color):
    print(color + msg + RESET)

def generate_graphs(episodes, avgScores, epLengths, epDurations):
    plt.figure(figsize=(8, 6))

    plt.xlim([0, np.max(episodes)])
    plt.xlabel('Episode')
    plt.ylabel('Average episode score')
    plt.title('Episode reward over time')

    plt.plot(episodes, avgScores, color='firebrick', linewidth=1.5)
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Learning curve.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, np.max(epDurations)])
    plt.xlabel('Time step')
    plt.ylabel('Episode')
    plt.title('Episode per time step')

    plt.plot(epDurations, episodes, color='firebrick', linewidth=1.5)
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Episodes duration.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, np.max(episodes)])
    plt.xlabel('Episode')
    plt.ylabel('Average episode length')
    plt.title('Episode length over time')

    plt.plot(episodes, epLengths, color='firebrick', linewidth=1.5)
    plt.savefig('/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/Episodes length.png')

    # from scipy import interpolate
    #
    # f = interpolate.make_interp_spline(episodes, avgScores)
    # episodes_smooth = np.linspace(episodes.min(), episodes.max(), episodes.size * 2)
    #
    # plt.plot(episodes_smooth, f(episodes_smooth), color='firebrick', linewidth=1.5)

def generate_graphs_for_comparison(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, folder, label1, label2):
    plt.figure(figsize=(8, 6))

    plt.xlim([0, max([np.max(episodes) for episodes in episodes_set])])
    plt.xlabel('Episode')
    plt.ylabel('Average episode score')
    plt.title('Episode reward over time')

    for idx, episodes in enumerate(episodes_set):
        plt.plot(episodes, avg_scores_set[idx], color="firebrick" if idx < int(len(episodes_set)/2) else "dodgerblue", linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label=label1)
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label=label2)
    plt.legend(loc="lower right")
    plt.savefig(f'/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/{folder}/Learning curve.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, max([np.max(avg_durations) for avg_durations in avg_durations_set])])
    plt.xlabel('Time step')
    plt.ylabel('Episode')
    plt.title('Episode per time step')

    for idx, avg_durations in enumerate(avg_durations_set):
        plt.plot(avg_durations, episodes_set[idx], color='firebrick' if idx < int(len(episodes_set)/2) else 'dodgerblue', linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label=label1)
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label=label2)
    plt.legend(loc="lower right")
    plt.savefig(f'/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/{folder}/Episodes duration.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, max([np.max(episodes) for episodes in episodes_set])])
    plt.xlabel('Episode')
    plt.ylabel('Average episode length')
    plt.title('Episode length over time')

    for idx, episodes in enumerate(episodes_set):
        plt.plot(episodes, avg_lengths_set[idx], color='firebrick' if idx < int(len(episodes_set)/2) else 'dodgerblue', linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label=label1)
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label=label2)
    plt.legend(loc="upper right")
    plt.savefig(f'/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/{folder}/Episodes length.png')

def get_average_data_to_plot(scores, lengths, durations):
    avgScores = np.array([])
    avgLengths = np.array([])
    avgDurations = np.array([])

    for i in range(1, EPISODES+1):
        if i % AGGREGATE_STATS_EVERY == 0:
            average_reward = sum(scores[i-AGGREGATE_STATS_EVERY:i]) / len(scores[i-AGGREGATE_STATS_EVERY:i])
            average_length = sum(lengths[i-AGGREGATE_STATS_EVERY:i]) / len(lengths[i-AGGREGATE_STATS_EVERY:i])
            average_duration = sum(durations[i-AGGREGATE_STATS_EVERY:i]) / len(durations[i-AGGREGATE_STATS_EVERY:i])

            avgScores = np.append(avgScores, average_reward)
            avgLengths = np.append(avgLengths, average_length)
            avgDurations = np.append(avgDurations, average_duration if not avgDurations.size else avgDurations[-1] + average_duration)

    return np.arange(AGGREGATE_STATS_EVERY, avgScores.size * AGGREGATE_STATS_EVERY + AGGREGATE_STATS_EVERY, step=AGGREGATE_STATS_EVERY), avgScores, avgLengths, avgDurations

def write_data(data, folder, dataType, idx):
    f = open(f"/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Data/{folder}/{dataType}-{idx}", 'w')
    for i, x in enumerate(data):
        if i == 0: f.write(f"[{x}")
        elif i == len(data) - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()

def read_data(folder, dataType, idx):
    f = open(f"/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Data/{folder}/{dataType}-{idx}", 'r')
    aux = f.readline().split(',')
    f.close()
    return np.array([float(re.sub('[\[\]]', '', e)) for e in aux])