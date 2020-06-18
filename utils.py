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

colors_graph = ["firebrick", "dodgerblue", "darkorchid", "forestgreen"]

def colorPrint(msg, color):
    print(color + msg + RESET)

def set_graph_parameters(plt, title, xlabel, ylabel, xbounds=None, ybounds=None, logscale=False):
    if xbounds is not None:
        plt.xlim(xbounds)
    if ybounds is not None and not logscale:
        plt.ylim(ybounds)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

def save_graph(plt, title, xlabel, ylabel, xdata, ydata, filename, xbounds=None, ybounds=None, logscale=False):
    plt.clf()
    set_graph_parameters(plt, title, xlabel, ylabel, xbounds, ybounds, logscale)

    if logscale:
        plt.yscale('log')
        plt.yticks(ticks=[0.1, 1, int(max(ydata))+1], labels=[0.1, 1, int(max(ydata))+1])

    plt.plot(xdata, ydata, color='firebrick', linewidth=1.5)
    plt.savefig(filename)

    # from scipy import interpolate
    #
    # f = interpolate.make_interp_spline(episodes, avgScores)
    # episodes_smooth = np.linspace(episodes.min(), episodes.max(), episodes.size * 2)
    #
    # plt.plot(episodes_smooth, f(episodes_smooth), color='firebrick', linewidth=1.5)

def save_comparison_graph(plt, title, xlabel, ylabel, xdata_set, ydata_set, labels, filename, separators, xbounds=None, ybounds=None, legendloc='lower right', logscale=False):
    plt.clf()
    set_graph_parameters(plt, title, xlabel, ylabel, xbounds, ybounds, logscale)

    if logscale:
        plt.yscale('log')
        plt.yticks(ticks=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1],
                   labels=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1])

    for i, sp in enumerate(separators):
        mean_data, min_data, max_data = calculate_mean_min_max(ydata_set, separators[i-1] if i > 0 else 0, sp)

        color = colors_graph[i]
        plt.plot(xdata_set[0], mean_data, color=color, linewidth=.8)
        plt.fill_between(xdata_set[0], min_data, max_data, alpha=.3, facecolor=color)

        plt.plot([], [], color=color, linewidth=1.5, label=labels[i])

    plt.legend(loc=legendloc)
    plt.savefig(filename)

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