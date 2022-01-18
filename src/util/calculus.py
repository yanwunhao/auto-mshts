import numpy as np
import math
from scipy.optimize import curve_fit


def calculate_summary_of_sample(sample):
    sample = np.array(sample, dtype=float)
    return np.sum(sample)


# definition of  sigmoid curve
def sigmoid_curve(x, a, b):
    return 1. / (1.0 + np.exp(-a * (x - b)))


# fit sigmoid curve with least squares method
def fit_sigmoid_curve(x_series, y_series):
    log_of_x = []
    for x in x_series:
        log_of_x.append(math.log(x, 10))

    y_series = np.array(y_series, dtype=float)
    popt, pcov = curve_fit(sigmoid_curve, log_of_x, y_series, maxfev=5000)

    x_sampling = np.linspace(np.min(log_of_x), np.max(log_of_x), 1000)
    y_sampling = sigmoid_curve(x_sampling, *popt)

    error_of_y_sampling = []
    for y in y_sampling:
        error_of_y_sampling.append(abs(y - 0.5))
    min_error = np.min(error_of_y_sampling)
    min_index = error_of_y_sampling.index(min_error)
    ec50 = sigmoid_curve(x_sampling[min_index], *popt)

    return x_sampling[min_index], ec50, x_sampling, y_sampling
