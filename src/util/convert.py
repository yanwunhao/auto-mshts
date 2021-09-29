import numpy as np


def split_array_into_samples(rebuild_array, sample_width, sample_height):
    sample_columns_number = int(48 / sample_width)
    sample_lines_number = int(32 / sample_height)

    sample_based_list = []

    for i in range(0, sample_columns_number):
        for j in range(0, sample_lines_number):
            temp = rebuild_array[j * sample_height:(j + 1) * sample_height, i * sample_width:(i + 1) * sample_width]
            sample_based_list.append(temp)

    return sample_based_list


def calculate_avg_of_sample(sample_array, sample_width, basic_width):
    calculate_data = sample_array.T
    times = int(sample_width / basic_width)

    sample_based_average_list = []

    for i in range(times):
        temp = calculate_data[i * basic_width:(i + 1) * basic_width, ]
        avg = np.array(temp, dtype=float).sum() / (2 * basic_width)
        sample_based_average_list.append(avg)

    return sample_based_average_list
