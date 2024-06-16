import pandas as pd

close_collisions_file_path = "C:/Users/dominykas.pleseviciu/Desktop/BigDataExam/close_collisions.csv"

df = pd.read_csv(close_collisions_file_path)

# Find the 5 closest collisions
df = df.sort_values(by="distance")
df = df.head(5)

print(df)

# We see that the collision is between vessels with MMSI 266334000 and 265388000 at 2021-12-13 10:43:56