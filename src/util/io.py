import csv
import numpy as np
import json


def read_setting_json():
    with open('./data/setting.json') as setting_f:
        setting = json.loads(setting_f.read())
        setting_f.close()
    return setting


def read_0h_data():
    with open('./data/0h.csv') as oh_data_f:
        csv_reader = csv.reader(oh_data_f)
        rows = [row for row in csv_reader]
        data = rows
        oh_data_f.close()
    flatten_data = np.array(data).flatten()
    return flatten_data


def read_24h_data():
    with open('./data/24h.csv') as oneday_data_f:
        csv_reader = csv.reader(oneday_data_f)
        rows = [row for row in csv_reader]
        data = rows
        oneday_data_f.close()
    flatten_data = np.array(data).flatten()
    return flatten_data
