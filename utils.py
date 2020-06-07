import numpy as np
import re


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

    for idx, episodes in enumerate(xdata_set):
        plt.plot(episodes, ydata_set[idx], color="firebrick" if idx < idxlim else "dodgerblue", linewidth=.8)

    plt.plot([], [], color="firebrick", linewidth=1.5, label=label1)
    plt.plot([], [], color="dodgerblue", linewidth=1.5, label=label2)
    plt.legend(loc=legendloc)
    plt.savefig(filename)

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