import numpy as np

class Matrix:
    def __init__(self, locations):
        self.dict_matrix_ = self.InitializeDictMatrix(locations)
        self.locations_ = locations

    def InitializeDictMatrix(self, locations):
        dict_matrix = {}
        for origin in locations:
            if origin.GetName() not in dict_matrix.keys():
                dict_matrix[origin.GetName()] = {}

            for destination in locations:
                dict_matrix[origin.GetName()][destination.GetName()] = 0.0
        return dict_matrix

    def GetDict(self):
        return self.dict_matrix_

    def GetArray(self):
        n_locations = len(self.locations_)
        array_matrix = np.zeros((n_locations, n_locations), dtype=np.float32)
        for origin_i, origin in enumerate(self.locations_):
            for destination_i, destination in enumerate(self.locations_):
                array_matrix[origin_i][destination_i] = self.dict_matrix_[origin.GetName()][destination.GetName()]
        return array_matrix

    def Set(self, key_i, key_j, val):
        self.dict_matrix_[key_i][key_j] = val
