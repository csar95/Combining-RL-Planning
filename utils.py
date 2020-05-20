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

def plot_graph(avgScores, episodes):
    plt.figure(figsize=(8, 6))
    # colors = ['darkorange', 'forestgreen', 'royalblue', 'firebrick', 'gold', 'deepskyblue', 'darkviolet', 'peru', 'deeppink', 'yellowgreen']

    plt.xlim([0, np.max(episodes)])
    # plt.ylim([0.0, 1.0])
    plt.xlabel('Episode')
    plt.ylabel('Average score')
    plt.title('Learning curve')
    # plt.legend(loc="lower right")

    # plt.scatter(episodes, avgScores)
    #
    # z = np.polyfit(episodes, avgScores, 1)
    # p = np.poly1d(z)
    # plt.plot(episodes, p(episodes), color='darkorange', linewidth=2)

    plt.plot(episodes, avgScores, color='darkorange', linewidth=2)  #, label=f'Label ')

    plt.show()
