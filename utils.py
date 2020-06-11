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

def save_comparison_graph(plt, title, xlabel, ylabel, xdata_set, ydata_set, label1, label2, filename, idxlim, xbounds=None, ybounds=None, legendloc='lower right', logscale=False):
    plt.clf()
    set_graph_parameters(plt, title, xlabel, ylabel, xbounds, ybounds, logscale)

    if logscale:
        plt.yscale('log')
        plt.yticks(ticks=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1],
                   labels=[0.1, 1, int(max([np.max(ydata) for ydata in ydata_set]))+1])



    mean_data1, min_data1, max_data1, mean_data2, min_data2, max_data2 = calculate_mean_min_max(ydata_set, idxlim)

    plt.plot(xdata_set[0], mean_data1, color="firebrick", linewidth=.8)
    plt.fill_between(xdata_set[0], min_data1, max_data1, alpha=.3, facecolor='firebrick')

    plt.plot(xdata_set[idxlim], mean_data2, color="dodgerblue", linewidth=.8)
    plt.fill_between(xdata_set[idxlim], min_data2, max_data2, alpha=.3, facecolor='dodgerblue')

    plt.plot([], [], color="firebrick", linewidth=1.5, label=label1)
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label=label2)
    plt.legend(loc=legendloc)
    plt.savefig(filename)

def calculate_mean_min_max(data_set, idxlim):
    mean_data1, mean_data2 = np.array([]), np.array([])
    min_data1, min_data2 = np.array([]), np.array([])
    max_data1, max_data2 = np.array([]), np.array([])

    for ep in range(data_set[0].size):
        data1, data2 = [], []

        for i in range(len(data_set)):
            if i < idxlim:
                data1.append(data_set[i][ep])
            else:
                data2.append(data_set[i][ep])

        mean_data1, mean_data2 = np.append(mean_data1, mean(data1)), np.append(mean_data2, mean(data2))
        min_data1, min_data2 = np.append(min_data1, min(data1)), np.append(min_data2, min(data2))
        max_data1, max_data2 = np.append(max_data1, max(data1)), np.append(max_data2, max(data2))

    return mean_data1, min_data1, max_data1, mean_data2, min_data2, max_data2

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