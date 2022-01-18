from util.io import read_setting_json, read_0h_data, read_24h_data, draw_single_curve
from util.convert import split_array_into_samples, calculate_avg_of_sample, convert_to_percentage
from util.calculus import calculate_summary_of_sample, fit_sigmoid_curve

import matplotlib.pyplot as plt
import numpy as np

setting = read_setting_json()
setting = setting["rule"]

# load experiment parameter
# experiment parameter is stored in file of ./data/setting.json
initial_filename = setting["0h_datafile"]
final_filename = setting["24h_datafile"]

# sample width and height are the size of each sample area
sample_width = setting["sample_width"]
sample_height = setting["sample_height"]
dilution_protocol = setting["dilution_protocol"]

# width of each dilution
basic_width = setting["basic_width"]

# number of each control group
control_number_list = setting["control_number"]

# load raw data
initial_sd_data = read_0h_data()
final_sd_data = read_24h_data()

# reshape data into the size of board
rebuild_0h_data = initial_sd_data.reshape((32, -1))
rebuild_24h_data = final_sd_data.reshape((32, -1))

# reshape data into a 2-dimensional array contains each group data
sample_divided_list_0h = split_array_into_samples(rebuild_0h_data, sample_width, sample_height)
sample_divided_list_24h = split_array_into_samples(rebuild_24h_data, sample_width, sample_height)

# handle data of control groups
control_0h_summary = 0
for number in control_number_list:
    number = number - 1
    sample = sample_divided_list_0h[number]
    control_0h_summary = control_0h_summary + calculate_summary_of_sample(sample)

control_0h_average = control_0h_summary / (sample_width * sample_height * len(control_number_list))

control_24h_summary = 0
for number in control_number_list:
    number = number - 1
    sample = sample_divided_list_24h[number]
    control_24h_summary = control_24h_summary + calculate_summary_of_sample(sample)

control_24h_average = control_24h_summary / (sample_width * sample_height * len(control_number_list))

# calculate standard deviation of each grid
sd_matrix = []
for line in rebuild_24h_data:
    new_line = []
    for element in line:
        sd_data = (float(element) - control_0h_average.item()) \
                  / (control_24h_average.item() - control_0h_average.item())
        new_line.append(sd_data)
    sd_matrix.append(new_line)

sd_matrix = np.array(sd_matrix)

# split array into different samples
sd_groups = split_array_into_samples(sd_matrix, sample_width, sample_height)
sd_groups = np.array(sd_groups, dtype=float)

RESULT_LIST = []
for sample in sd_groups:
    result = calculate_avg_of_sample(sample, sample_width, basic_width)
    RESULT_LIST.append(result)

RESULT_LIST = np.array(RESULT_LIST)

FULL_RESULT_LIST = []

for group in sd_groups:
    x_index = 0
    y_index = 0
    sample_buffer = []
    data_buffer = []
    while y_index < sample_height:
        while x_index < basic_width:
            x = x_index
            while x < sample_width:
                data_buffer.append(group[y_index][x])
                x += basic_width
            sample_buffer.append(data_buffer)
            data_buffer = []
            x_index += 1
        y_index += 1
        x_index = 0
    FULL_RESULT_LIST.append(sample_buffer)

FULL_RESULT_LIST = np.array(FULL_RESULT_LIST, dtype=float)

x_data = [300, 60, 12, 2.4, 0.48, 0.096]

optional_color = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

sample_num = 0
for SAMPLE in FULL_RESULT_LIST:
    sample_num += 1
    fig, ax = plt.subplots()
    index = 0
    ax.set_title('Sample '+str(sample_num))

    x_buffer = []
    x_sampling_buffer = []
    y_sampling_buffer = []

    for repeat in SAMPLE:
        x, y, x_sampling, y_sampling = fit_sigmoid_curve(x_data, repeat)
        x_buffer.append(x)
        x_sampling_buffer.append(x_sampling)
        y_sampling_buffer.append(y_sampling)
        draw_single_curve(ax, x, y, x_sampling, y_sampling, optional_color[index])
        index += 1

    avg = np.mean(x_buffer)

    x_sampling_buffer = np.array(x_sampling_buffer).T
    y_sampling_buffer = np.array(y_sampling_buffer).T

    x_sampling_avg = []
    y_sampling_avg = []

    for line in x_sampling_buffer:
        x_sampling_avg.append(np.mean(line))

    for line in y_sampling_buffer:
        y_sampling_avg.append(np.mean(line))

    ax.plot(avg, 0.5, 'o', color='black')
    ax.plot(x_sampling_avg, y_sampling_avg, color='black')
    ax.legend()
    plt.show()
