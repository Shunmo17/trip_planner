import googlemaps

import modules.common_util as common_util
from modules.day import Day
from modules.params import *

class Trip:
    def __init__(self, config_path, location_path, n_days, location_header=LOCATION_HEADER, pkl_path=PICKLE_PATH):
        result, config = common_util.LoadYaml(config_path)
        if not result:
            raise FileNotFoundError("Failed to load config file")

        result, self.base_days_ = common_util.LoadPickle(pkl_path)
        if result:
            print("succeeded to load pickle")

        api_key = config["google_map"]["api_key"]
        self.gmaps_ = googlemaps.Client(key=api_key)

        self.days_ = self.SetDays(location_path, n_days, self.base_days_)

        if len(self.days_) > 0:
            self.UpdateCsv(self.days_, location_path, location_header)

        common_util.SavePickle(pkl_path, self.days_)

    def SetDays(self, location_path, n_days, base_days):
        days = []
        for day_i in range(n_days):
            if base_days is not None and len(base_days) > day_i:
                days.append(Day(self.gmaps_, location_path, day=day_i, base=base_days[day_i]))
            else:
                days.append(Day(self.gmaps_, location_path, day=day_i))
        return days

    def UpdateCsv(self, days, location_path, location_header):
        location_list = []
        for day in days:
            location_list.extend(day.GetCsvWriteData())
        common_util.SaveCsv(location_path, location_header, location_list)



Trip(CONFIG_PATH, LOCATION_PATH, N_DAYS)
