import pulp

import modules.common_util as common_util
from modules.matrix import Matrix
from modules.location import Location
from modules.params import *

class Day:
    def __init__(self, gmaps, location_path, day=None, base=None):
        if day is not None:
            print("##############################################")
            print("##                   DAY {}                  ##".format(day + 1))
            print("##############################################")
        self.need_update_csv_ = False
        self.gmaps_ = gmaps
        self.locations_ = self.LoadLocation(location_path, day)
        self.locations_ = self.SetLatitudeAndLongitude(self.locations_)
        self.distance_matrix_ = Matrix(self.locations_)
        self.time_matrix_ = Matrix(self.locations_)

        if len(self.locations_) > 0:
            self.distance_matrix_, self.time_matrix_ = self.SetDistanceTimeMatrix(self.distance_matrix_, self.time_matrix_, base)

        self.PlanningRoute()

    def SetLatitudeAndLongitude(self, locations):
        for location in locations:
            if location.GetLatitude() == "" or location.GetLongitude() == "":
                result = self.gmaps_.geocode(location.GetAddress())
                print("########## USE GOOGLE MAP API (geocode) ##########")
                latitude = result[0]["geometry"]["location"]["lat"]
                longitude = result[0]["geometry"]["location"]["lng"]
                location.SetLatitude(latitude)
                location.SetLongitude(longitude)
                print("{} was set to ({:.2f}, {:.2f})".format(location.GetName(), latitude, longitude))
            else:
                # print("{} is already set longitude and latitude".format(location.GetName()))
                pass
        return locations

    def LoadLocation(self, location_path, day):
        locations = []
        result, location_datas = common_util.LoadCsv(location_path)
        if not result:
            raise FileNotFoundError("Failed to load location file")

        for location_data in location_datas:
            if location_data["day"] == "":
                raise RuntimeError("The day of {} was not set!".format(location_data["name"]))
            if day is None or (type(day) is int and int(location_data["day"]) - 1 == day):
                locations.append(Location(location_data))
            else:
                RuntimeError("Invalid day: {}".format(day))
        return locations

    def GetCsvWriteData(self):
        locations_list = []
        for location in self.locations_:
            location_list = []
            location_list.append(location.GetName())
            location_list.append(location.GetDay())
            location_list.append(location.GetAddress())
            location_list.append(location.GetLatitude())
            location_list.append(location.GetLongitude())
            locations_list.append(location_list)
        return locations_list

    def SetDistanceTimeMatrix(self, distance_matrix, time_matrix, base=None):
        for origin in self.locations_:
            for destination in self.locations_:
                if origin.GetName() != destination.GetName():
                    distance = -100.0
                    time = -100.0
                    # if the distance was already calculated, use the calculated value
                    if base is not None and \
                            origin.GetName() in base.GetDistanceMatrix().GetDict().keys() and \
                            destination.GetName() in base.GetDistanceMatrix().GetDict()[origin.GetName()].keys():
                        distance = base.GetDistanceMatrix().GetDict()[origin.GetName()][destination.GetName()]
                        time = base.GetTimeMatrix().GetDict()[origin.GetName()][destination.GetName()]
                        # print("use calculated value: ({}) --> ({})".format(origin.GetName(), destination.GetName()))
                    else:
                        origin_geometry = (origin.GetLatitude(), origin.GetLongitude())
                        destination_geometry = (destination.GetLatitude(), destination.GetLongitude())
                        result = self.gmaps_.distance_matrix(origin_geometry, destination_geometry, mode=TRAVEL_MODE)
                        print("########## USE GOOGLE MAP API (distancematrix) ##########")
                        distance = result["rows"][0]["elements"][0]["distance"]["value"]
                        time = result["rows"][0]["elements"][0]["duration"]["value"]
                    distance_matrix.Set(origin.GetName(), destination.GetName(), distance)
                    time_matrix.Set(origin.GetName(), destination.GetName(), time)
        return distance_matrix, time_matrix

    def PlanningRoute(self):
        n_location = len(self.locations_)
        prob = pulp.LpProblem('tsp')

        # initialize variables
        xs = []
        for i in range(n_location):
            xs1 = [pulp.LpVariable("{}--{}".format(self.locations_[i].GetName(), self.locations_[j].GetName()), cat='Binary') for j in range(n_location)]
            xs.append(xs1)
        us = [pulp.LpVariable("{}".format(self.locations_[i].GetName()), cat='Integer', lowBound=0, upBound=n_location - 1) for i in range(n_location)]

        # objective function
        # prob += pulp.lpSum([pulp.lpDot(w, x) for w, x in zip(self.distance_matrix_.GetArray(), xs)])
        prob += pulp.lpSum([pulp.lpDot(w, x) for w, x in zip(self.time_matrix_.GetArray(), xs)])

        # constraints
        for i in range(n_location):
            prob += pulp.lpSum([xs[j][i] for j in range(n_location)]) == 1
            prob += pulp.lpSum([xs[i][j] for j in range(n_location)]) == 1

        # 自分自身への辺は選択しない
        for i in range(n_location):
            prob += xs[i][i] == 0

        # 頂点に対応する変数の制約
        for i in range(n_location):
            for j in range(1, n_location):
                if i == j:
                    continue
                prob += us[i] + 1 - (n_location - 1) * (1 - xs[i][j]) <= us[j]

        prob += us[0] == 0                 # スタート
        for i in range(1, n_location):
            prob += 1 <= us[i]

        status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
        # print("Status", pulp.LpStatus[status])
        # print("z", prob.objective.value())
        # get result
        route = [None for _ in range(n_location)]
        for i, u in enumerate(us):
            route[int(u.value())] = self.locations_[i]

        tot_distance = 0.0
        tot_time_sec = 0.0
        for i in range(n_location):
            orig_i = i
            if i < n_location - 1:
                dest_i = i + 1
            else:
                dest_i = 0
            origin, destination = route[orig_i], route[dest_i]
            print(origin.GetName())
            distance = self.distance_matrix_.GetDict()[origin.GetName()][destination.GetName()] / 1000.0
            tot_distance += distance
            t_sec = self.time_matrix_.GetDict()[origin.GetName()][destination.GetName()]
            tot_time_sec += t_sec
            hour, min = t_sec // 3600.0, (t_sec % 3600.0) // 60.0
            print(" | {}: {:.1f} km ({:.0f}時間{:.0f}分)".format(TRAVEL_MODE_JP, distance, hour, min))
        print(route[0].GetName())
        tot_time_hour, tot_time_min = tot_time_sec // 3600.0, (tot_time_sec % 3600.0) // 60.0
        print("---------------------------")
        print("総移動距離: {:.3f} km".format(tot_distance))
        print("所要時間:   {:.0f}時間{:.0f}分".format(tot_time_hour, tot_time_min))
        print("---------------------------")




    def GetDistanceMatrix(self):
        return self.distance_matrix_

    def GetTimeMatrix(self):
        return self.time_matrix_
