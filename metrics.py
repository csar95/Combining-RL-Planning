from hyperparameters import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import os


class Metrics:

    def __init__(self, scores=None, lengths=None, durations=None, avgLoss=None, avgAccuracy=None):
        self.scores = [] if scores is None else scores
        self.lengths = [] if lengths is None else lengths
        self.durations = [] if durations is None else durations
        self.avgLoss = [] if avgLoss is None else avgLoss
        self.avgAccuracy = [] if avgAccuracy is None else avgAccuracy

    def add(self, episode_score, episode_length, episode_duration, episode_avgLoss=None, episode_avgAccuracy=None):
        self.scores.append(episode_score)
        self.lengths.append(episode_length)
        self.durations.append(episode_duration)
        if episode_avgLoss is not None:
            self.avgLoss.append(episode_avgLoss)
        if episode_avgAccuracy is not None:
            self.avgAccuracy.append(episode_avgAccuracy)

    def get_average_data(self, segment, idx=None):
        if idx is None:
            idx = len(self.scores)

        average_reward = sum(self.scores[idx-segment:idx]) / len(self.scores[idx-segment:idx])
        average_length = sum(self.lengths[idx-segment:idx]) / len(self.lengths[idx-segment:idx])
        average_duration = sum(self.durations[idx-segment:idx]) / len(self.durations[idx-segment:idx])

        if len(self.avgLoss) > 0 and len(self.avgAccuracy) > 0:
            suma = list(filter(lambda loss: loss != 0, self.avgLoss[idx-segment:idx]))
            average_loss = sum(suma) / len(suma)

            suma = list(filter(lambda accuracy: accuracy != 0, self.avgAccuracy[idx-segment:idx]))
            average_accuracy = sum(suma) / len(suma)

            return average_reward, average_length, average_duration, average_loss, average_accuracy
        else:
            return average_reward, average_length, average_duration, None, None

    def get_average_data_to_plot(self):
        avgScores = np.array([])
        avgLengths = np.array([])
        avgDurations = np.array([])
        avgLoss = np.array([])
        avgAccuracy = np.array([])

        for i in range(1, EPISODES+1):
            if i % SHOW_STATS_EVERY == 0:
                average_reward, average_length, average_duration, average_loss, average_accuracy = \
                    self.get_average_data(SHOW_STATS_EVERY, i)

                avgScores = np.append(avgScores, average_reward)
                avgLengths = np.append(avgLengths, average_length)
                avgDurations = np.append(avgDurations, average_duration if not avgDurations.size else avgDurations[-1] + average_duration)
                avgLoss = np.append(avgLoss, average_loss)
                avgAccuracy = np.append(avgAccuracy, average_accuracy)

        return np.arange(SHOW_STATS_EVERY, avgScores.size * SHOW_STATS_EVERY + SHOW_STATS_EVERY, step=SHOW_STATS_EVERY), avgScores, avgLengths, avgDurations, avgLoss, avgAccuracy

    def save_data(self, folder, idx):
        pathtodata = f"{DATA_FOLDER}{folder}/{idx}"
        if not os.path.isdir(pathtodata):
            os.makedirs(pathtodata)

        write_data(self.scores, pathtodata, "scores")
        write_data(self.scores, pathtodata, "lengths")
        write_data(self.scores, pathtodata, "durations")
        write_data(self.scores, pathtodata, "avgLoss")
        write_data(self.scores, pathtodata, "avgAccuracy")

    def plot_results(self, plot_avg_loss_accuracy=True):
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_accuracy = self.get_average_data_to_plot()

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
                   xdata=episodes if plot_avg_loss_accuracy else np.arange(np.max(episodes) - len(self.avgLoss), np.max(episodes)),
                   ydata=avg_loss if plot_avg_loss_accuracy else self.avgLoss,
                   filename=f"{FIGURES_FOLDER}Episodes loss.png", logscale=True)

        # EPISODES ACCURACY ------------------------------------------------------------------------------------------ #

        save_graph(plt, title='Episode average accuracy over time', xlabel='Episode', ylabel='Average episode accuracy',
                   xbounds=[0, np.max(episodes)], ybounds=[0,1],
                   xdata=episodes if plot_avg_loss_accuracy else np.arange(np.max(episodes) - len(self.avgAccuracy), np.max(episodes)),
                   ydata=avg_accuracy if plot_avg_loss_accuracy else self.avgAccuracy,
                   filename=f"{FIGURES_FOLDER}Episodes accuracy.png")

    @staticmethod
    def plot_results_for_comparison(comparison_folder, label1, label2, episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, avg_loss_set, avg_accuracy_set, idxlim):
        plt.figure(figsize=(8, 6))

        # LEARNING CURVE --------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode reward over time', xlabel='Episode', ylabel='Average episode score',
                              xdata_set=episodes_set, ydata_set=avg_scores_set, label1=label1, label2=label2,
                              filename=f"{FIGURES_FOLDER}{comparison_folder}/Learning curve.png", idxlim=idxlim,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])])

        # EPISODES LENGTH -------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode length over time', xlabel='Episode', ylabel='Average episode length',
                              xdata_set=episodes_set, ydata_set=avg_lengths_set, label1=label1, label2=label2,
                              filename=f"{FIGURES_FOLDER}{comparison_folder}/Episodes length.png", idxlim=idxlim,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])], legendloc='upper right')

        # EPISODES DURATION ------------------------------------------------------------------------------------------ #

        save_comparison_graph(plt, title='Episode per time step', xlabel='Time step', ylabel='Episode',
                              xdata_set=avg_durations_set, ydata_set=episodes_set, label1=label1, label2=label2,
                              idxlim=idxlim, filename=f"{FIGURES_FOLDER}{comparison_folder}/Episodes duration.png",
                              xbounds=[0, max([np.max(avg_durations) for avg_durations in avg_durations_set])])

        # EPISODES LOSS ---------------------------------------------------------------------------------------------- #

        save_comparison_graph(plt, title='Episode average loss over time', xlabel='Episode', ylabel='Average episode loss',
                              xdata_set=episodes_set, ydata_set=avg_loss_set, label1=label1, label2=label2,
                              filename=f"{FIGURES_FOLDER}{comparison_folder}/Episodes loss.png", idxlim=idxlim,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])],
                              legendloc='upper right', logscale=True)

        # EPISODES ACCURACY ------------------------------------------------------------------------------------------ #

        save_comparison_graph(plt, title='Episode average accuracy over time', xlabel='Episode', ylabel='Average episode accuracy',
                              xdata_set=episodes_set, ydata_set=avg_accuracy_set, label1=label1, label2=label2,
                              filename=f"{FIGURES_FOLDER}{comparison_folder}/Episodes accuracy.png", idxlim=idxlim,
                              xbounds=[0, max([np.max(episodes) for episodes in episodes_set])], ybounds=[0,1])

