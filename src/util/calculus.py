import numpy as np


def calculate_summary_of_sample(sample):
    sample = np.array(sample, dtype=float)
    return np.sum(sample)
