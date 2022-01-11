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
    popt, pcov = curve_fit(sigmoid_curve, log_of_x, y_series)
    y_series_fit = sigmoid_curve(log_of_x, *popt)

    x_sampling = np.linspace(np.min(log_of_x), np.max(log_of_x), 1000)
    y_sampling = sigmoid_curve(x_sampling, *popt)

    error_of_y_sampling = []
    for y in y_sampling:
        error_of_y_sampling.append(abs(y - 0.5))
    min_error = np.min(error_of_y_sampling)
    min_index = error_of_y_sampling.index(min_error)
    ec50 = math.pow(10, x_sampling[min_index])

    return x_sampling[min_index], ec50, y_series_fit, x_sampling, y_sampling


test_x = [300, 60, 12, 2.4, 0.48, 0.096]

test_data_group = [
    [2.892885861, 27.66910071, 71.84552934, 74.43030153, 69.1593526, 88.99740895],
    [2.694920211, 27.28574799, 63.01986173, 67.70942829, 69.536698, 81.30974886],
    [1.208480025, 30.97319569, 76.76797761, 69.44912388, 73.03067554, 86.87139297],
    [7.475780468, 31.43207988, 81.37388562, 70.00504512, 81.63855574, 74.28814157]
]

test_data_group = np.array(test_data_group, dtype=float)
test_data_group = test_data_group / 100.

for data in test_data_group:
    x, y, y_series_fit, x_sampling, y_sampling = fit_sigmoid_curve(test_x, data)
