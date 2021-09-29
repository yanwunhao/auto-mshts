from util.io import read_setting_json, read_0h_data, read_24h_data
from util.convert import split_array_into_samples, calculate_avg_of_sample


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

