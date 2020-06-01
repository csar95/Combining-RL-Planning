import matplotlib.pyplot as plt
import numpy as np


RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
GREY = "\x1b[90m"
RESET = "\x1b[0m"

RESOURCES_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Encoding_Module/Resources/"

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

def write_episodes(episodes, idx, path):
    f = open(f"{path}/episodes-{idx}", 'w')
    for i, x in enumerate(episodes):
        if i == 0: f.write(f"[{x}")
        elif i == episodes.size - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()

def write_avg_scores(avg_scores, idx, path):
    f = open(f"{path}/avg_scores-{idx}", 'w')
    for i, x in enumerate(avg_scores):
        if i == 0: f.write(f"[{x}")
        elif i == avg_scores.size - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()

def write_avg_lengths(avg_lengths, idx, path):
    f = open(f"{path}/avg_lengths-{idx}", 'w')
    for i, x in enumerate(avg_lengths):
        if i == 0: f.write(f"[{x}")
        elif i == avg_lengths.size - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()

def write_avg_durations(avg_durations, idx, path):
    f = open(f"{path}/avg_durations-{idx}", 'w')
    for i, x in enumerate(avg_durations):
        if i == 0: f.write(f"[{x}")
        elif i == avg_durations.size - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()
