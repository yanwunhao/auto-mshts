import numpy as np


def calculate_control_denominator(data_0h, data_24h):
    return np.array(data_24h) - np.array(data_0h)


def calculate_average_for_each_index(source_arr):
    source_arr = np.array(source_arr)
    return np.mean(source_arr, axis=0)