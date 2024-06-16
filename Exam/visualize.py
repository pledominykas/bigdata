import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

processed_data_folder_path = "C:/Users/dominykas.pleseviciu/Desktop/BigDataExam/aisdk-2021-12-processed"
visualize_minutes_before = 45
visualize_minutes_after = 30

# Define the MMSI and timestamp of the vessel collision
mmsi1 = 266334000
mmsi2 = 265388000
timestamp = datetime.strptime("2021-12-13 10:43:56", "%Y-%m-%d %H:%M:%S")

# Load the processed data
df = pd.read_csv(processed_data_folder_path + "/aisdk-2021-12-13.csv", names=["timestamp", "mmsi", "latitude", "longitude"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Filter the data to the specified MMSIs
df = df[(df["mmsi"] == mmsi1) | (df["mmsi"] == mmsi2)]

# Filter the data to the specified time range
start_time = timestamp - pd.Timedelta(minutes=visualize_minutes_before)
end_time = timestamp + pd.Timedelta(minutes=visualize_minutes_after)
df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

# Plot the data
plt.figure(figsize=(10, 6))
for mmsi, group in df.groupby("mmsi"):
    plt.plot(group["longitude"], group["latitude"], label=mmsi, linestyle="--")

    # Mark start and end points
    plt.scatter(group.iloc[0]["longitude"], group.iloc[0]["latitude"], color="red")
    plt.scatter(group.iloc[-1]["longitude"], group.iloc[-1]["latitude"], color="green")
    plt.annotate(f"Start ({group.iloc[0]['timestamp']})", (group.iloc[0]["longitude"], group.iloc[0]["latitude"]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"End ({group.iloc[-1]['timestamp']})", (group.iloc[-1]["longitude"], group.iloc[-1]["latitude"]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Vessel Positions")
plt.legend()
plt.show()