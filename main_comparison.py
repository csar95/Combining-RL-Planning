from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DDQL_elevators_p4"
    data_folder2 = "DDQL_elevators_p4 (RP_3)"
    comparison_folder = "DDQL_elevators_p4_Comparision_StandardvsPlanReuse (RP_3_Half)"
    label1 = "DDQL"
    label2 = "DDQL w/ Plan Reuse"

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []
    avg_loss_set = []
    avg_accuracy_set = []

    for i in range(2):
        pathtodata = f"{DATA_FOLDER}{data_folder1}/{i}"

        scores = read_data(pathtodata, "scores")
        lengths = read_data(pathtodata, "lengths")
        durations = read_data(pathtodata, "durations")
        avgLoss = read_data(pathtodata, "avgLoss")
        avgAccuracy = read_data(pathtodata, "avgAccuracy")

        data = Metrics(scores, lengths, durations, avgLoss, avgAccuracy)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_accuracy = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)
        avg_accuracy_set.append(avg_accuracy)

    for i in range(3,5):
        pathtodata = f"{DATA_FOLDER}{data_folder2}/{i}"

        scores = read_data(pathtodata, "scores")
        lengths = read_data(pathtodata, "lengths")
        durations = read_data(pathtodata, "durations")
        avgLoss = read_data(pathtodata, "avgLoss")
        avgAccuracy = read_data(pathtodata, "avgAccuracy")

        data = Metrics(scores, lengths, durations, avgLoss, avgAccuracy)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_accuracy = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)
        avg_accuracy_set.append(avg_accuracy)

    Metrics.plot_results_for_comparison(comparison_folder, label1, label2, episodes_set, avg_scores_set,
                                        avg_lengths_set, avg_durations_set, avg_loss_set, avg_accuracy_set, idxlim=2)

# episodes_set.append(episodes[:80])
# avg_scores_set.append(avg_scores[:80])
# avg_lengths_set.append(avg_lengths[:80])
# avg_durations_set.append(avg_durations[:80])
# avg_loss_set.append(avg_loss[:80])
# avg_accuracy_set.append(avg_accuracy[:80])

# episodes_set.append(episodes)
# avg_scores_set.append(avg_scores)
# avg_lengths_set.append(avg_lengths)
# avg_durations_set.append(avg_durations)
# avg_loss_set.append(avg_loss)
# avg_accuracy_set.append(avg_accuracy)