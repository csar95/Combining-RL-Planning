from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DoubleDQL"
    data_folder2 = "DDQL_PR_3"
    comparison_folder = "DDQL_vs_DDQL_PR_3"
    label1 = "Double DQL"
    label2 = "DDQL w/ Plan Reuse (3)"

    episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, avg_loss_set, avg_fscore_set = [], [], [], [], [], []

    for i in range(3):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder1}/{i}"

        scores, lengths, durations, avgLoss, avgFScore = read_data(pathtodata, "scores"), read_data(pathtodata, "lengths"), \
                                                         read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss"), \
                                                         read_data(pathtodata, "avgFScore")

        data = Metrics(scores, lengths, durations, avgLoss, avgFScore)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_fscore = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)
        avg_fscore_set.append(avg_fscore)

    for i in range(1):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder2}/{i}"

        scores, lengths, durations, avgLoss, avgFScore = read_data(pathtodata, "scores"), read_data(pathtodata, "lengths"), \
                                                         read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss"), \
                                                         read_data(pathtodata, "avgFScore")

        data = Metrics(scores, lengths, durations, avgLoss, avgFScore)
        episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_fscore = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)
        avg_fscore_set.append(avg_fscore)

    Metrics.plot_results_for_comparison(comparison_folder, label1, label2, episodes_set, avg_scores_set,
                                        avg_lengths_set, avg_durations_set, avg_loss_set, avg_fscore_set, idxlim=3)

# episodes_set.append(episodes[:80])
# avg_scores_set.append(avg_scores[:80])
# avg_lengths_set.append(avg_lengths[:80])
# avg_durations_set.append(avg_durations[:80])
# avg_loss_set.append(avg_loss[:80])
# avg_fscore_set.append(avg_fscore[:80])

# episodes_set.append(episodes)
# avg_scores_set.append(avg_scores)
# avg_lengths_set.append(avg_lengths)
# avg_durations_set.append(avg_durations)
# avg_loss_set.append(avg_loss)
# avg_fscore_set.append(avg_fscore)