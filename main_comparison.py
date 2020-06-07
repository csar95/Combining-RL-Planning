from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DDQL_elevators_p4"
    data_folder2 = "DDQL_elevators_p4 (Prev. Plans)"
    comparison_folder = "DDQL_elevators_p4_Comparision_StandardvsPlanReuse"
    label1 = "DDQL"
    label2 = "DDQL w/ Plan Reuse"

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []
    avg_loss_set = []
    avg_accuracy_set = []

    for i in range(1,3):
        scores = read_data(data_folder1, "scores", i)
        lengths = read_data(data_folder1, "lengths", i)
        durations = read_data(data_folder1, "durations", i)
        avgLoss = read_data(data_folder1, "avgLoss", i)
        avgAccuracy = read_data(data_folder1, "avgAccuracy", i)

        data = Metrics(scores, lengths, durations, avgLoss, avgAccuracy)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_accuracy = data.get_average_data_to_plot()

        episodes_set.append(episodes[:80])
        avg_scores_set.append(avg_scores[:80])
        avg_lengths_set.append(avg_lengths[:80])
        avg_durations_set.append(avg_durations[:80])
        avg_loss_set.append(avg_loss[:80])
        avg_accuracy_set.append(avg_accuracy[:80])

    for i in range(1,3):
        scores = read_data(data_folder2, "scores", i)
        lengths = read_data(data_folder2, "lengths", i)
        durations = read_data(data_folder2, "durations", i)
        avgLoss = read_data(data_folder2, "avgLoss", i)
        avgAccuracy = read_data(data_folder2, "avgAccuracy", i)

        data = Metrics(scores, lengths, durations, avgLoss, avgAccuracy)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_accuracy = data.get_average_data_to_plot()

        episodes_set.append(episodes[:80])
        avg_scores_set.append(avg_scores[:80])
        avg_lengths_set.append(avg_lengths[:80])
        avg_durations_set.append(avg_durations[:80])
        avg_loss_set.append(avg_loss[:80])
        avg_accuracy_set.append(avg_accuracy[:80])

    Metrics.plot_results_for_comparison(comparison_folder, label1, label2, episodes_set, avg_scores_set,
                                        avg_lengths_set, avg_durations_set, avg_loss_set, avg_accuracy_set, idxlim=2)