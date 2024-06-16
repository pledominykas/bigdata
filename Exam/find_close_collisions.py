import os
import csv
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from multiprocessing import Pool
from multiprocessing import cpu_count
from datetime import datetime

processed_data_folder_path = "C:/Users/dominykas.pleseviciu/Desktop/BigDataExam/aisdk-2021-12-processed"
files = os.listdir(processed_data_folder_path)
num_processes = cpu_count()

# From Task 3 histogram of delta t, we saw that majority of the data is within 10 seconds
# We consider collision if the distance between two vessels is less than 30 meters within 10 seconds
collision_distance_threshold = 0.03
collision_seconds_threshold = 10

# Code from: https://stackoverflow.com/a/15737218
def haversine_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    km = 6371* c

    return km

def find_closest_vessels(file_path):
    close_collisions = []

    # Data in the file is sorted by timestamp
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        close_vessels_in_time = []
        row_count = 0

        for row in reader:
            timestamp = datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S")
            mmsi = row[1]
            latitude = float(row[2])
            longitude = float(row[3])

            # Remove vessels that are too far in time if the timestamp is too old
            if(len(close_vessels_in_time) > 0 and close_vessels_in_time[-1]["timestamp"] < timestamp):
                close_vessels_in_time = [vessel for vessel in close_vessels_in_time if (timestamp - vessel["timestamp"]).seconds < collision_seconds_threshold]

            # Check for vessels that are too close
            for vessel in close_vessels_in_time:
                distance = haversine_distance(vessel["longitude"], vessel["latitude"], longitude, latitude)
                if vessel["mmsi"] != mmsi and distance < collision_distance_threshold:
                    close_collisions.append((mmsi, vessel["mmsi"], timestamp, distance))

            # Add the current vessel to the list
            close_vessels_in_time.append({
                "timestamp": timestamp,
                "mmsi": mmsi,
                "latitude": latitude,
                "longitude": longitude
            })

            # Print progress
            row_count += 1
            if row_count % 50000 == 0:
                print(f"Processed {row_count} rows in {file_path}")

    return close_collisions


if __name__ == "__main__":
    with Pool(num_processes) as p:
        close_collisions = p.map(find_closest_vessels, [processed_data_folder_path + "/" + file for file in files])

    close_collisions = [collision for collisions in close_collisions for collision in collisions]

    close_collisions_df = pd.DataFrame(close_collisions, columns=["mmsi1", "mmsi2", "timestamp", "distance"])
    close_collisions_df.to_csv("close_collisions.csv", index=False)