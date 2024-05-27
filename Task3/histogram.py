from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


client = MongoClient('mongodb://localhost:27019')
db = client['big_data_db']
collection = db['filtered_vessels']


vessels = list(collection.find())


grouped_vessels = {}
for vessel in vessels:
    if vessel['mmsi'] not in grouped_vessels:
        grouped_vessels[vessel['mmsi']] = []
    grouped_vessels[vessel['mmsi']].append(vessel)

for mmsi, vessel_data in grouped_vessels.items():
    grouped_vessels[mmsi] = sorted(vessel_data, key=lambda x: datetime.strptime(x['timestamp'], '%d/%m/%Y %H:%M:%S'))



grouped_delta_ts = {}
for mmsi, vessel_data in grouped_vessels.items():
    for i in range(1, len(vessel_data)):
        time_curr = datetime.strptime(vessel_data[i]['timestamp'], '%d/%m/%Y %H:%M:%S')
        time_prev = datetime.strptime(vessel_data[i - 1]['timestamp'], '%d/%m/%Y %H:%M:%S')

        delta_t = time_curr.timestamp() - time_prev.timestamp()

        if mmsi not in grouped_delta_ts:
            grouped_delta_ts[mmsi] = []
        grouped_delta_ts[mmsi].append(delta_t)


all_delta_ts = []
for mmsi, delta_ts in grouped_delta_ts.items():
    all_delta_ts.extend(delta_ts)

plt.hist(all_delta_ts, bins=50)
plt.title('Delta t histogram for all vessels')
plt.pause(100)

# for mmsi, delta_ts in grouped_delta_ts.items():
#     plt.hist(delta_ts, bins=50)
#     plt.title(f'Delta t histogram for vessel {mmsi}')
#     plt.xlabel('Delta t (s)')
#     plt.ylabel('Frequency')
#     plt.show()