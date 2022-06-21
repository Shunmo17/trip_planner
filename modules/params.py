import os

# path to files
CONFIG_PATH = os.path.dirname(__file__) + "/../config.yaml"
LOCATION_PATH = os.path.dirname(__file__) + "/../location.csv"
PICKLE_PATH = os.path.dirname(__file__) + "/../days.pkl"

# header definition
LOCATION_HEADER = ["name", "day", "address", "latitude", "longitude"]

# travel method
TRAVEL_MODE = "driving"
TRAVEL_MODE_JP = "車移動"

# ther number of days
N_DAYS = 1
