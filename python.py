import csv
import json
from math import asin, cos, radians, sin, sqrt

SENSOR_FILE_CSV = "SensorData1.csv"
SENSOR_FILE_JSON = "SensorData2.json"
SENSOR_FILE_OUTPUT = "SensorOutput.json"
SENSOR_ACCURACY = 100  # meters

# (id, lat, long)
csv_sensor_data = []
with open(SENSOR_FILE_CSV, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip header
    next(csv_reader)

    for row in csv_reader:
        sensor_id = int(row[0])
        lat = float(row[1])
        long = float(row[2])
        csv_sensor_data.append((sensor_id, lat, long))

# (id, lat, long)
json_sensor_data = []
with open(SENSOR_FILE_JSON, "r") as json_file:
    data = json.load(json_file)
    for sensor in data:
        sensor_id = int(sensor["id"])
        lat = float(sensor["latitude"])
        long = float(sensor["longitude"])
        json_sensor_data.append((sensor_id, lat, long))


# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


candidate_pairs = {}
for sensor_csv in csv_sensor_data:
    for sensor_json in json_sensor_data:
        dist = (
            haversine(sensor_csv[2], sensor_csv[1], sensor_json[2], sensor_json[1])
            * 1000
        )

        # If distance between 2 anomalies is less than the sensor accuracy
        # Could be a candidate
        if dist <= SENSOR_ACCURACY:
            candidate_pairs[sensor_csv[0]] = sensor_json[0]

# Save result
with open(SENSOR_FILE_OUTPUT, "w") as output_file:
    json.dump(candidate_pairs, output_file)
