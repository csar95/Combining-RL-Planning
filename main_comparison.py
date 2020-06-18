from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DoubleDQL_Soft-Update (0.01)"
    data_folder2 = "DDQL_PR_3"
    data_folder3 = "DDQL_PR_3 (Lite)"
    data_folder4 = "DDQL_PR_6"
    comparison_folder = "DDQL_vs_DDQL_PR_3_vs_DDQL_PR_3_Lite_vs_DDQL_PR_6"
    labels = ["Double DQL", "DDQL w/ Plan Reuse (3)", "DDQL w/ Plan Reuse (3 - Lite)", "DDQL w/ Plan Reuse (6)"]

    episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, avg_loss_set, avg_fscore_set = [], [], [], [], [], []

    for i in range(2,5):
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

    for i in range(2):
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

    for i in range(3):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder3}/{i}"

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

    for i in range(3):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder4}/{i}"

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

    Metrics.plot_results_for_comparison(comparison_folder, labels, episodes_set, avg_scores_set,
                                        avg_lengths_set, avg_durations_set, avg_loss_set, avg_fscore_set, separators=[3,5,8,11])
