class Location:
    def __init__(self, csv_row):
        self.name_ = csv_row["name"]
        self.day_ = csv_row["day"]
        self.address_ = csv_row["address"]
        self.latitude_ = csv_row["latitude"]
        self.longitude_ = csv_row["longitude"]
        self.day_ = csv_row["day"]

    def GetName(self):
        return self.name_

    def GetAddress(self):
        return self.address_

    def GetLatitude(self):
        return self.latitude_

    def GetLongitude(self):
        return self.longitude_

    def GetDay(self):
        return self.day_

    def SetLatitude(self, latitude):
        if -180 <= latitude <= 180:
            self.latitude_ = latitude
        else:
            raise RuntimeError("Latitude = {:.2f} is out of range".format(latitude))

    def SetLongitude(self, longitude):
        if -180 <= longitude <= 180:
            self.longitude_ = longitude
        else:
            raise RuntimeError("Longitude = {:.2f} is out of range".format(longitude))
