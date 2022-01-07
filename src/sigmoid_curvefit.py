import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x_data = [300, 60, 12, 2.4, 0.48, 0.096]

log_of_x_data = []

for x in x_data:
    log_of_x_data.append(math.log(x, 10))

y_data_group = [
    [2.892885861, 27.66910071, 71.84552934, 74.43030153, 69.1593526, 88.99740895],
    [2.694920211, 27.28574799, 63.01986173, 67.70942829, 69.536698, 81.30974886],
    [1.208480025, 30.97319569, 76.76797761, 69.44912388, 73.03067554, 86.87139297],
    [7.475780468, 31.43207988, 81.37388562, 70.00504512, 81.63855574, 74.28814157]
]


def sigmoid(x, a, b):
    return 1. / (1.0 + np.exp(-a * (x - b)))


for y_data in y_data_group:
    y_data = np.array(y_data)
    y_data = y_data / 100.

    popt, pcov = curve_fit(sigmoid, log_of_x_data, y_data)
    output_y = sigmoid(log_of_x_data, *popt)

    sampling_x = np.linspace(np.min(log_of_x_data), np.max(log_of_x_data), 1000)
    sampling_y = sigmoid(sampling_x, *popt)

    error_of_sampling_y = []
    for y in sampling_y:
        error_of_sampling_y.append(abs(y - 0.5))
    min_error = np.min(error_of_sampling_y)
    min_index = error_of_sampling_y.index(min_error)
    ec50 = math.pow(10, sampling_x[min_index])
    print('EC50 is ' + str(ec50))
