import csv
import json
import pickle
import requests
import yaml

def LoadYaml(yaml_path):
    data = None
    try:
        with open(yaml_path, 'r', encoding="shift_jis") as file:
            data = yaml.safe_load(file)
        return True, data
    except FileNotFoundError:
        return False, data

def LoadCsv(csv_path):
    list_data = []
    try:
        with open(csv_path, 'r', encoding="shift_jis") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                list_data.append(row)
            return True, list_data
    except FileNotFoundError:
        return False, list_data

def LoadPickle(pickle_path):
    obj_data = None
    try:
        with open(pickle_path, mode="rb") as file:
            obj_data = pickle.load(file)
        return True, obj_data
    except FileNotFoundError:
        return False, obj_data

def SaveCsv(csv_path, header, list_data):
    with open(csv_path, 'w', encoding="shift_jis", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(list_data)

def SavePickle(pickle_path, obj_data):
    try:
        with open(pickle_path, mode="wb") as file:
            pickle.dump(obj_data, file)
        return True
    except FileNotFoundError:
        return False
