from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DoubleDQL_Hard-Update (500)"
    data_folder2 = "DoubleDQL"
    # data_folder3 = "DoubleDQL_Hard-Update (50)"
    # data_folder4 = "DoubleDQL_Hard-Update (0.5)"
    comparison_folder = "Hard-Update_vs_Soft-Update"
    labels = ["Hard-Update (Frecuency = 500)", "Soft-Update (TAU = 0.005)", "", ""]

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

    for i in range(3):
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

    # for i in range(3):
    #     pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder3}/{i}"
    #
    #     scores, lengths, durations, avgLoss, avgFScore = read_data(pathtodata, "scores"), read_data(pathtodata, "lengths"), \
    #                                                      read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss"), \
    #                                                      read_data(pathtodata, "avgFScore")
    #
    #     data = Metrics(scores, lengths, durations, avgLoss, avgFScore)
    #     episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_fscore = data.get_average_data_to_plot()
    #
    #     episodes_set.append(episodes)
    #     avg_scores_set.append(avg_scores)
    #     avg_lengths_set.append(avg_lengths)
    #     avg_durations_set.append(avg_durations)
    #     avg_loss_set.append(avg_loss)
    #     avg_fscore_set.append(avg_fscore)

    # for i in range(3):
    #     pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder4}/{i}"
    #
    #     scores, lengths, durations, avgLoss, avgFScore = read_data(pathtodata, "scores"), read_data(pathtodata, "lengths"), \
    #                                                      read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss"), \
    #                                                      read_data(pathtodata, "avgFScore")
    #
    #     data = Metrics(scores, lengths, durations, avgLoss, avgFScore)
    #     episodes, avg_scores, avg_lengths, avg_durations, avg_loss, avg_fscore = data.get_average_data_to_plot()
    #
    #     episodes_set.append(episodes)
    #     avg_scores_set.append(avg_scores)
    #     avg_lengths_set.append(avg_lengths)
    #     avg_durations_set.append(avg_durations)
    #     avg_loss_set.append(avg_loss)
    #     avg_fscore_set.append(avg_fscore)

    Metrics.plot_results_for_comparison(comparison_folder, labels, episodes_set, avg_scores_set,
                                        avg_lengths_set, avg_durations_set, avg_loss_set, avg_fscore_set, separators=[3,6])
