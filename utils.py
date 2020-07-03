import numpy as np
import re
from statistics import mean


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

# colors_graph = ["firebrick", "dodgerblue", "darkorchid", "forestgreen"]
# colors_graph = ["peru", "dimgrey"]
# colors_graph = ["peru", "purple", "dimgrey"]
# colors_graph = ["peru", "purple", "dodgerblue", "teal", "dimgrey"]
colors_graph = ["peru", "purple", "dodgerblue", "dimgrey"]

def colorPrint(msg, color):
    print(color + msg + RESET)

def set_graph_parameters(axs, pos, title, xlabel, ylabel, xbounds=None, ybounds=None, logscale=False):
    if xbounds is not None:
        axs[pos].set_xlim(xbounds)
    if ybounds is not None and not logscale:
        axs[pos].set_ylim(ybounds)

    axs[pos].set_xlabel(xlabel, fontsize=13)
    axs[pos].set_ylabel(ylabel, fontsize=13)
    axs[pos].set_title(title, fontsize=15, pad=13)
    axs[pos].yaxis.set_ticks_position('both')

def save_comparison_graph(axs, pos, title, xdata_set, ydata_set, separators, ylabel, xlabel=None, xbounds=None, ybounds=None, logscale=False):
    set_graph_parameters(axs, pos, title, xlabel, ylabel, xbounds, ybounds, logscale)

    if logscale:
        axs[pos].set_yscale('log')
        axs[pos].set_yticks(ticks=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1])
        axs[pos].set_yticklabels(labels=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1])

    for i, sp in enumerate(separators):
        # mean_data, min_data, max_data = calculate_mean_min_max(ydata_set, separators[i-1] if i > 0 else 0, sp)
        mean_data, st_quartile, rd_quartile = calculate_interquartile_range(ydata_set, separators[i - 1] if i > 0 else 0, sp)

        color = colors_graph[i]
        axs[pos].plot(xdata_set[0], mean_data, color=color, linewidth=1.2)
        axs[pos].spines['top'].set_visible(False)
        # axs[x,y].fill_between(xdata_set[0], min_data, max_data, alpha=.35, facecolor=color, edgecolor=color)
        axs[pos].fill_between(xdata_set[0], st_quartile, rd_quartile, alpha=.35, facecolor=color, edgecolor=color)

    axs[pos].grid(linestyle='dotted', color='black')

def calculate_mean_min_max(data_set, lim1, lim2):
    mean_data = np.array([]), np.array([])
    min_data = np.array([]), np.array([])
    max_data  = np.array([]), np.array([])

    for ep in range(data_set[0].size):
        data = []

        for i in range(len(data_set)):
            if lim1 <= i < lim2:
                data.append(data_set[i][ep])

        mean_data = np.append(mean_data, mean(data))
        min_data = np.append(min_data, min(data))
        max_data = np.append(max_data, max(data))

    return mean_data, min_data, max_data

def calculate_interquartile_range(data_set, lim1, lim2):
    mean_data = np.array([]), np.array([])
    fst_data = np.array([]), np.array([])
    lst_data  = np.array([]), np.array([])

    for ep in range(data_set[0].size):
        data = []

        for i in range(len(data_set)):
            if lim1 <= i < lim2:
                data.append(data_set[i][ep])

        mean_data = np.append(mean_data, mean(data))
        fst_data = np.append(fst_data, np.percentile(data, 10))
        lst_data = np.append(lst_data, np.percentile(data, 90))

    return mean_data, fst_data, lst_data

def write_data(data, folder, dataType):
    f = open(f"{folder}/{dataType}", 'w')
    for i, x in enumerate(data):
        if i == 0: f.write(f"[{x}")
        elif i == len(data) - 1: f.write(f",{x}]")
        else: f.write(f",{x}")
    f.close()

def read_data(folder, dataType):
    f = open(f"{folder}/{dataType}", 'r')
    aux = f.readline().split(',')
    f.close()
    return np.array([float(re.sub('[\[\]]', '', e)) for e in aux])