from metrics import *
from utils import *


if __name__ == '__main__':
    data_folder1 = "DoubleDQL_Hard-Update (500)"
    data_folder2 = "DoubleDQL_Hard-Update (100)" # "DDQL_PR_3"         "DoubleDQL_Soft-Update (0.01)" "DoubleDQL_Hard-Update (500)"   "DDQL_PER (0.1)"    "DDQL_2ndEncoding (Z-score norm.)"  "DDQL_PR_1 (0.2)"
    data_folder3 = "DoubleDQL_Hard-Update (50)"  # "DDQL_PR_3 (Lite)"  "DoubleDQL_Soft-Update (0.1)"  "DoubleDQL_Hard-Update (100)"   "DDQL_PER (0.7)"    "DDQL_2ndEncoding (NO norm.)"       "DDQL_PR_1 (0.8)"
    data_folder4 = "DQL" # "DDQL_PR_6"         "DoubleDQL_Soft-Update (0.5)"  "DoubleDQL_Hard-Update (50)"    "DDQL_PER (0.9)"    "DDQL_2ndEncoding (Min-Max norm.)"  "DDQL_PR_1"

    # figure_name = "DoubleDQL_Hard-Update"
    # figure_name = "DoubleDQL_Soft-Update"
    # figure_name = "DDQL_vs_DQL"
    # figure_name = "DDQL_vs_DDQL_PER"
    # figure_name = "1stEncoding_vs_2ndEncoding"
    # figure_name = "DDQL_vs_DDQL_PR_3_vs_DDQL_PR_3_Lite_vs_DDQL_PR_6"
    figure_name = "DQL_&_DDQL_Hard-Update"

    labels = ["Frecuency = 500", "Frecuency = 100", "Frecuency = 50", "DQL"]
    # labels = ["TAU = 0.005", "TAU = 0.01", "TAU = 0.1", "TAU = 0.5", "DQL"]
    # labels = ["Double DQL", "DQL"]
    # labels = ["Double DQL", "Double DQL w/ PER (a=0.1)", "Double DQL w/ PER (a=0.7)", "Double DQL w/ PER (a=0.9)"]
    # labels = ["DDQL (1st encoding)", "DDQL (2nd encoding - Z-score)", "DDQL (2nd encoding - No norm.)", "DDQL (2nd encoding - Min-Max)"]
    # labels = ["Double DQL", "DDQL w/ Plan Reuse (1 - Reuse = 0.2)", "DDQL w/ Plan Reuse (1 - Reuse = 0.8)"]
    # labels = ["Double DQL", "DDQL w/ Plan Reuse (3)", "DDQL w/ Plan Reuse (3 - Lite)", "DDQL w/ Plan Reuse (6)"]

    episodes_set, avg_scores_set, avg_durations_set, avg_loss_set = [], [], [], []

    for i in range(5):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder1}/{i}"

        scores, durations, avgLoss = read_data(pathtodata, "scores"), read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss")

        data = Metrics(scores=scores, durations=durations, avgLoss=avgLoss)
        episodes, avg_scores, _, avg_durations, avg_loss, _ = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)

    for i in range(5):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder2}/{i}"

        scores, durations, avgLoss = read_data(pathtodata, "scores"), read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss")

        data = Metrics(scores=scores, durations=durations, avgLoss=avgLoss)
        episodes, avg_scores, _, avg_durations, avg_loss, _ = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)

    for i in range(5):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder3}/{i}"

        scores, durations, avgLoss = read_data(pathtodata, "scores"), read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss")

        data = Metrics(scores=scores, durations=durations, avgLoss=avgLoss)
        episodes, avg_scores, _, avg_durations, avg_loss, _ = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)

    for i in range(5):
        pathtodata = f"{DATA_FOLDER}{PROBLEM}/{data_folder4}/{i}"

        scores, durations, avgLoss = read_data(pathtodata, "scores"), read_data(pathtodata, "durations"), read_data(pathtodata, "avgLoss")

        data = Metrics(scores=scores, durations=durations, avgLoss=avgLoss)
        episodes, avg_scores, _, avg_durations, avg_loss, _ = data.get_average_data_to_plot()

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_durations_set.append(avg_durations)
        avg_loss_set.append(avg_loss)

    Metrics.plot_results_for_comparison(figure_name, labels, episodes_set, avg_scores_set, avg_durations_set, avg_loss_set, separators=[5,10,15,20])
