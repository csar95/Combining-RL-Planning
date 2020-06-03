from utils import *


if __name__ == '__main__':
    data_folder1 = "DDQL_elevators_p3"
    data_folder2 = ""
    comparison_folder = "DDQL_elevators_p3"
    label1 = "DDQL Hard update"
    label2 = ""

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []

    for i in range(3):
        episodes = read_data(data_folder1, "episodes", i)
        avg_scores = read_data(data_folder1, "avg_scores", i)
        avg_lengths = read_data(data_folder1, "avg_lengths", i)
        avg_durations = read_data(data_folder1, "avg_durations", i)

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)

    # for i in range(2):
    #     episodes = read_data(data_folder2, "episodes", i)
    #     avg_scores = read_data(data_folder2, "avg_scores", i)
    #     avg_lengths = read_data(data_folder2, "avg_lengths", i)
    #     avg_durations = read_data(data_folder2, "avg_durations", i)
    #
    #     episodes_set.append(episodes)
    #     avg_scores_set.append(avg_scores)
    #     avg_lengths_set.append(avg_lengths)
    #     avg_durations_set.append(avg_durations)

    generate_graphs_for_comparison(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, comparison_folder, label1, label2)