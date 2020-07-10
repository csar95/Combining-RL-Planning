from hyperparameters import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import os


class Metrics:

    def __init__(self, scores=None, lengths=None, durations=None, avgLoss=None, avgFScore=None):
        self.scores = [] if scores is None else scores
        self.lengths = [] if lengths is None else lengths
        self.durations = [] if durations is None else durations
        self.avgLoss = [] if avgLoss is None else avgLoss
        self.avgFScore = [] if avgFScore is None else avgFScore

    def add(self, episode_score, episode_length, episode_duration, episode_avgLoss=None, episode_avgFScore=None):
        self.scores.append(episode_score)
        self.lengths.append(episode_length)
        self.durations.append(episode_duration)
        if episode_avgLoss is not None:
            self.avgLoss.append(episode_avgLoss)
        if episode_avgFScore is not None:
            self.avgFScore.append(episode_avgFScore)

    def get_average_data(self, segment, idx=None):
        if idx is None:
            idx = len(self.scores)

        average_reward = sum(self.scores[idx-segment:idx]) / len(self.scores[idx-segment:idx])
        average_duration = sum(self.durations[idx-segment:idx]) / len(self.durations[idx-segment:idx])
        average_length, average_loss, average_fscore = None, None, None

        if len(self.lengths) > 0:
            average_length = sum(self.lengths[idx-segment:idx]) / len(self.lengths[idx-segment:idx])

        if len(self.avgLoss) > 0:
            suma = list(filter(lambda loss: loss != 0, self.avgLoss[idx-segment:idx]))
            if suma: average_loss = sum(suma) / len(suma)

        if len(self.avgFScore) > 0:
            suma = list(filter(lambda fscore: fscore != 0, self.avgFScore[idx - segment:idx]))
            if suma: average_fscore = sum(suma) / len(suma)

        return average_reward, average_length, average_duration, average_loss, average_fscore

    def get_average_data_to_plot(self):
        avgScores, avgLengths, avgDurations, avgLoss, avgFScore = np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

        for i in range(1, EPISODES+1):
            if i % SHOW_STATS_EVERY == 0:
                average_reward, average_length, average_duration, average_loss, average_fscore = \
                    self.get_average_data(SHOW_STATS_EVERY, i)

                avgScores = np.append(avgScores, average_reward)
                avgLengths = np.append(avgLengths, average_length)
                avgDurations = np.append(avgDurations, sum(self.durations[:i]))
                avgLoss = np.append(avgLoss, average_loss)
                avgFScore = np.append(avgFScore, average_fscore)

        return np.arange(SHOW_STATS_EVERY, avgScores.size * SHOW_STATS_EVERY + SHOW_STATS_EVERY, step=SHOW_STATS_EVERY), avgScores, avgLengths, avgDurations, avgLoss, avgFScore

    def save_data(self, folder, idx):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{folder}/{idx}"
        if not os.path.isdir(pathtodata):
            os.makedirs(pathtodata)

        write_data(self.scores, pathtodata, "scores")
        write_data(self.lengths, pathtodata, "lengths")
        write_data(self.durations, pathtodata, "durations")
        if len(self.avgLoss) > 0:
            write_data(self.avgLoss, pathtodata, "avgLoss")
        if len(self.avgFScore) > 0:
            write_data(self.avgFScore, pathtodata, "avgFScore")

    @staticmethod
    def plot_results_for_comparison(figure_name, labels, episodes_set, avg_scores_set, durations_set, avg_loss_set, separators):
        pathtofigures = f"{FIGURES_FOLDER}{PROBLEM}/"
        if not os.path.isdir(pathtofigures):
            os.makedirs(pathtofigures)

        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(24,7))
        plt.subplots_adjust(top=0.91, bottom=0.17, left=0.04, right=0.98, wspace=0.13)

        # LEARNING CURVE --------------------------------------------------------------------------------------------- #

        save_comparison_graph(axs, 0, title='Episode reward over time', xlabel='Episode', ylabel='Reward',
                              xdata_set=episodes_set, ydata_set=avg_scores_set, separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])], ybounds=[-400, 800])

        # EPISODES DURATION ------------------------------------------------------------------------------------------ #

        save_comparison_graph(axs, 1, title='Running time', xlabel='Episode', ylabel='Time (s)',
                              xdata_set=episodes_set, ydata_set=durations_set, separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])],
                              ybounds=[0, 450])

        # EPISODES LOSS ---------------------------------------------------------------------------------------------- #

        save_comparison_graph(axs, 2, title='Episode average loss over time', xlabel='Episode', ylabel='Average episode loss',
                              xdata_set=episodes_set, ydata_set=avg_loss_set, separators=separators, logscale=True,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])],
                              ybounds=[min([np.min(loss) for loss in avg_loss_set]), max([np.max(loss) for loss in avg_loss_set])])

        # Set figure labels and legend
        for i, sp in enumerate(separators):
            axs[0].plot([], [], color=colors_graph[i], linewidth=2, label=labels[i])
        fig.legend(loc="lower center", ncol=len(separators), edgecolor="black", prop={'size': 17})

        # Save image
        plt.savefig(f"{pathtofigures}{figure_name}.png")