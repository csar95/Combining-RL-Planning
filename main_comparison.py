from utils import *


if __name__ == '__main__':
    folder1 = "DoubleDQL"
    folder2 = "DoubleDQL_PER"
    folder3 = "Comparison_DDQLvsDDQL_PER"

    episodes_set = []
    avg_scores_set = []
    avg_lengths_set = []
    avg_durations_set = []

    for i in range(5):
        episodes = read_data(folder1, "episodes", i)
        avg_scores = read_data(folder1, "avg_scores", i)
        avg_lengths = read_data(folder1, "avg_lengths", i)
        avg_durations = read_data(folder1, "avg_durations", i)

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)

    for i in range(5):
        episodes = read_data(folder2, "episodes", i)
        avg_scores = read_data(folder2, "avg_scores", i)
        avg_lengths = read_data(folder2, "avg_lengths", i)
        avg_durations = read_data(folder2, "avg_durations", i)

        episodes_set.append(episodes)
        avg_scores_set.append(avg_scores)
        avg_lengths_set.append(avg_lengths)
        avg_durations_set.append(avg_durations)

    generate_graphs_for_comparison(episodes_set, avg_scores_set, avg_lengths_set, avg_durations_set, folder3)