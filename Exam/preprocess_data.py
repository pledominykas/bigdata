import os
import csv
from math import radians, cos, sin, asin, sqrt
from multiprocessing import Pool
from multiprocessing import cpu_count

data_folder_path = "C:/Users/dominykas.pleseviciu/Desktop/BigDataExam/aisdk-2021-12"
processed_data_folder_path = "C:/Users/dominykas.pleseviciu/Desktop/BigDataExam/aisdk-2021-12-processed"
num_processes = cpu_count()

files = os.listdir(data_folder_path)

circle_latitude = 55.225000
circle_longitude = 14.245000
circle_radius = 50

# Code from: https://stackoverflow.com/a/15737218
def haversine_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    km = 6371* c

    return km

def is_valid_entry(entry):
    return entry != "" and entry != "Undefined" and entry != "Unknown"

def preprocess_file(file_path):
    file_name = os.path.basename(file_path)
    processed_file_path = processed_data_folder_path + "/" + file_name
    row_number = 0

    # Open processed data file
    with(open(processed_file_path, 'w+')) as processed_file:
        # Open raw data file
        with open(file_path, 'r') as file:
            # Skip csv header
            next(file)

            reader = csv.reader(file)

            for row in reader:
                # Extract data
                vessel_timestamp = row[0]
                vessel_type = row[1]
                vessel_mmsi = row[2]
                vessel_latitude = float(row[3])
                vessel_longitude = float(row[4])
                vessel_nav_status = row[5]
                vessel_rot = row[6]
                vessel_sog = row[7]
                vessel_cog = row[8]

                # Latitude must be between -90 and 90, longitude must be between -180 and 180 for valid coordinates
                if(vessel_latitude < -90 or vessel_latitude > 90 or vessel_longitude < -180 or vessel_longitude > 180 or not is_valid_entry(vessel_mmsi) or not is_valid_entry(vessel_nav_status) or not is_valid_entry(vessel_rot) or not is_valid_entry(vessel_sog) or not is_valid_entry(vessel_cog)):
                    continue

                # Check if vessel is in circle
                if(haversine_distance(circle_longitude, circle_latitude, vessel_longitude, vessel_latitude) < circle_radius):
                    # Write data to processed file
                    processed_file.write(f"{vessel_timestamp},{vessel_mmsi},{vessel_latitude},{vessel_longitude}\n")

                if(row_number % 100000 == 0):
                    print(f"Processed {row_number} rows from {file_name} out of about 10 000 000 rows")

                row_number += 1

if __name__ == "__main__":
    with Pool(num_processes) as p:
        p.map(preprocess_file, [data_folder_path + "/" + file for file in files])