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
        average_length = sum(self.lengths[idx-segment:idx]) / len(self.lengths[idx-segment:idx])
        average_duration = sum(self.durations[idx-segment:idx]) / len(self.durations[idx-segment:idx])
        average_loss, average_fscore = None, None

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
                # avgDurations = np.append(avgDurations, average_duration if not avgDurations.size else avgDurations[-1] + average_duration)
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

    def plot_results(self, plot_avg_loss_fscore=True):
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_fscore = self.get_average_data_to_plot()

        plt.figure(figsize=(8, 6))

        # LEARNING CURVE --------------------------------------------------------------------------------------------- #

        save_graph(plt, title='Episode reward over time', xlabel='Episode', ylabel='Average episode score',
                   xbounds=[0, np.max(episodes)], xdata=episodes, ydata=avg_scores,
                   filename=f"{FIGURES_FOLDER}Learning curve.png")

        # EPISODES DURATION ------------------------------------------------------------------------------------------ #

        save_graph(plt, title='Episode per time step', xlabel='Time step', ylabel='Episode',
                   xbounds=[0, np.max(avg_durations)], xdata=avg_durations, ydata=episodes,
                   filename=f"{FIGURES_FOLDER}Episodes duration.png")

        # EPISODES LENGTH -------------------------------------------------------------------------------------------- #

        save_graph(plt, title='Episode length over time', xlabel='Episode', ylabel='Average episode length',
                   xbounds=[0, np.max(episodes)], xdata=episodes, ydata=avg_lengths,
                   filename=f"{FIGURES_FOLDER}Episodes length.png")

        # EPISODES LOSS ---------------------------------------------------------------------------------------------- #

        save_graph(plt, title='Episode average loss over time', xlabel='Episode', ylabel='Average episode loss',
                   xbounds=[0, np.max(episodes)],
                   xdata=episodes if plot_avg_loss_fscore else np.arange(np.max(episodes) - len(self.avgLoss), np.max(episodes)),
                   ydata=avg_loss if plot_avg_loss_fscore else self.avgLoss,
                   filename=f"{FIGURES_FOLDER}Episodes loss.png", logscale=True)

        # EPISODES F-SCORE ------------------------------------------------------------------------------------------- #

        save_graph(plt, title='Episode average F-score over time', xlabel='Episode', ylabel='Average episode F-score',
                   xbounds=[0, np.max(episodes)], ybounds=[0,1],
                   xdata=episodes if plot_avg_loss_fscore else np.arange(np.max(episodes) - len(self.avgFScore), np.max(episodes)),
                   ydata=avg_fscore if plot_avg_loss_fscore else self.avgFScore,
                   filename=f"{FIGURES_FOLDER}Episodes F-score.png")

    @staticmethod
    def plot_results_for_comparison(comparison_folder, labels, episodes_set, avg_scores_set, avg_lengths_set, durations_set, avg_loss_set, avg_fscore_set, separators):
        pathtofigures = f"{FIGURES_FOLDER}{PROBLEM}/{comparison_folder}/"
        if not os.path.isdir(pathtofigures):
            os.makedirs(pathtofigures)

        plt.figure(figsize=(8, 6))

        # LEARNING CURVE --------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode reward over time', xlabel='Episode', ylabel='Episode score',
                              xdata_set=episodes_set, ydata_set=avg_scores_set, labels=labels,
                              filename=f"{pathtofigures}Learning_Curve.png", separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])])

        # EPISODES LENGTH -------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode length over time', xlabel='Episode', ylabel='Episode length',
                              xdata_set=episodes_set, ydata_set=avg_lengths_set, labels=labels,
                              filename=f"{pathtofigures}Episodes_Length.png", separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])], legendloc='upper right')

        # EPISODES DURATION ------------------------------------------------------------------------------------------ #

        save_comparison_graph(plt, title='Computational time', xlabel='Episode', ylabel='Time (s)',
                              xdata_set=episodes_set, ydata_set=durations_set, labels=labels,
                              separators=separators, filename=f"{pathtofigures}Episodes_Duration.png",
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])],
                              ybounds=[0, max([np.max(durations) for durations in durations_set])])

        # EPISODES LOSS ---------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode average loss over time', xlabel='Episode', ylabel='Average episode loss',
                              xdata_set=episodes_set, ydata_set=avg_loss_set, labels=labels,
                              filename=f"{pathtofigures}Episodes_Avg_Loss.png", separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])],
                              legendloc='upper right', logscale=True)

        # EPISODES F-SCORE ------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode average F-score over time', xlabel='Episode', ylabel='Average episode F-score',
                              xdata_set=episodes_set, ydata_set=avg_fscore_set, labels=labels,
                              filename=f"{pathtofigures}Episodes_Avg_F-score.png", separators=separators,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])], ybounds=[0,1])

