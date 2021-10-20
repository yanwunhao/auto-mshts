from util.io import read_setting_json, read_0h_data, read_24h_data
from util.convert import split_array_into_samples, calculate_avg_of_sample, convert_to_percentage
from util.calculus import calculate_control_denominator, calculate_average_for_each_index, calculate_summary_of_sample

import numpy as np

setting = read_setting_json()
setting = setting["rule"]

# load experiment parameter
initial_filename = setting["0h_datafile"]
final_filename = setting["24h_datafile"]

sample_width = setting["sample_width"]
sample_height = setting["sample_height"]
dilution_protocol = setting["dilution_protocol"]
basic_width = setting["basic_width"]

control_number_list = setting["control_number"]

# load raw data
initial_sd_data = read_0h_data()
final_sd_data = read_24h_data()

rebuild_0h_data = initial_sd_data.reshape((32, -1))
rebuild_24h_data = final_sd_data.reshape((32, -1))

sample_divided_list_0h = split_array_into_samples(rebuild_0h_data, sample_width, sample_height)
sample_divided_list_24h = split_array_into_samples(rebuild_24h_data, sample_width, sample_height)

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


sd_matrix = []
for line in rebuild_24h_data:
    new_line = []
    for element in line:
        sd_data = (float(element) - control_0h_average.item()) \
                  / (control_24h_average.item() - control_0h_average.item())
        new_line.append(sd_data)
    sd_matrix.append(new_line)

sd_matrix = np.array(sd_matrix)

sd_groups = split_array_into_samples(sd_matrix, sample_width, sample_height)

RESULT_LIST = []
for sample in sd_groups:
    result = calculate_avg_of_sample(sample, sample_width, basic_width)
    RESULT_LIST.append(result)

RESULT_LIST = np.array(RESULT_LIST)
input()