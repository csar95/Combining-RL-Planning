from utils import *


if __name__ == '__main__':
    data_folder1 = ""
    data_folder2 = ""
    comparison_folder = ""
    label1 = ""
    label2 = ""

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []

    for i in range(1,2):
        scores = read_data(data_folder1, "scores", i)
        lengths = read_data(data_folder1, "lengths", i)
        durations = read_data(data_folder1, "durations", i)

        episodes, avg_scores, avg_lengths, avg_durations = get_average_data_to_plot(scores, lengths, durations)

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)

    for i in range(1,2):
        scores = read_data(data_folder1, "scores", i)
        lengths = read_data(data_folder1, "lengths", i)
        durations = read_data(data_folder1, "durations", i)

        episodes, avg_scores, avg_lengths, avg_durations = get_average_data_to_plot(scores, lengths, durations)

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)

    generate_graphs_for_comparison(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, comparison_folder, label1, label2)