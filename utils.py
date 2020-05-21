import matplotlib.pyplot as plt
import numpy as np

from Learning_Module.hyperparameters_DQL import *


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
    plt.savefig('Learning curve.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, np.max(epDurations)])
    plt.xlabel('Time step')
    plt.ylabel('Episode')
    plt.title('Episode per time step')

    plt.plot(epDurations, episodes, color='firebrick', linewidth=1.5)
    plt.savefig('Episodes duration.png')

    # ------------------------------------------------------------------------------------------------ #

    plt.clf()

    plt.xlim([0, np.max(episodes)])
    plt.xlabel('Episode')
    plt.ylabel('Average episode length')
    plt.title('Episode length over time')

    plt.plot(episodes, epLengths, color='firebrick', linewidth=1.5)
    plt.savefig('Episodes length.png')