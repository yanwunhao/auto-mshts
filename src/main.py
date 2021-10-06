from util.io import read_setting_json, read_0h_data, read_24h_data
from util.convert import split_array_into_samples, calculate_avg_of_sample, convert_to_percentage
from util.calculus import calculate_control_denominator, calculate_average_for_each_index


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

sample_based_list_0h = split_array_into_samples(rebuild_0h_data, sample_width, sample_height)

total_average_list_0h = []

for sample in sample_based_list_0h:
    total_average_list_0h.append(calculate_avg_of_sample(sample, sample_width, basic_width))

sample_based_list_24h = split_array_into_samples(rebuild_24h_data, sample_width, sample_height)

total_average_list_24h = []

for sample in sample_based_list_24h:
    total_average_list_24h.append(calculate_avg_of_sample(sample, sample_width, basic_width))

control_average_list_0h = []
control_average_list_24h = []
for number in setting["control_number"]:
    control_average_list_0h.append(total_average_list_0h[number])
    control_average_list_24h.append(total_average_list_24h[number])
control_denominator_list = calculate_control_denominator(control_average_list_0h, control_average_list_24h)

control_higher_average_list_0h = calculate_average_for_each_index(control_average_list_0h)
denominators_list = calculate_average_for_each_index(control_denominator_list)

RESULT_LIST = []

for sample in total_average_list_24h:
    i = 0
    result_of_sample = []
    for condition in sample:
        sd_of_condition = (condition - control_higher_average_list_0h[i]) / denominators_list[i]
        result_of_sample.append(sd_of_condition)
        i += 1
    RESULT_LIST.append(result_of_sample)

RESULT_LIST = convert_to_percentage(RESULT_LIST)

input()
