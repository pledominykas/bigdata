import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.functions import *
# from pyspark.sql.types import FloatType

spark = SparkSession.builder.appName("Spark-assignment 3").getOrCreate()
# spark = SparkSession.builder \
#     .appName("Spark-assignment 3") \
#     .config("spark.driver.memory", "4g") \
#     .config("spark.executor.memory", "4g") \
#     .config("spark.network.timeout", "800s") \
#     .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
#     .getOrCreate()


# 1) read data and ensure correct formats
df = spark.read.csv("C:/Users/polik/Desktop/VU stuff/Big Data/pythonProject/aisdk-2024-05-04.csv", header=True)

# check schema for correct types of latitude, longitude and timestamp
df.printSchema()

# change types of columns
df = df.withColumn('Latitude', df["Latitude"].cast('float')).\
        withColumn('Longitude', df["Longitude"].cast('float')).\
        withColumn('Timestamp', to_timestamp('# Timestamp', 'dd/MM/yyyy HH:mm:ss'))

df.printSchema()

vessels = df.select(['Timestamp', 'Latitude', 'Longitude', 'MMSI'])
vessels.show(5)

# 2.1) Calculate the distance between consecutive positions for each vessel
# using a suitable geospatial library or custom function that can integrate with PySpark.

# Unique identifiers of vessels are:
# MMSI -- used for communication and navigation
# IMO  -- used for vessel registration;
# for this task MMSI is used as identifier.

# Distance between two points on a perfect sphere -- Haversine formula
# https://en.wikipedia.org/wiki/Haversine_formula

# To find distance between two consecutive positions we need to use lagged coordinates:
# apply a window function partitioned by 'MMSI' and ordered by timestamp
window_spec = Window.partitionBy("MMSI").orderBy("Timestamp")

# add previous coordinates columns
vessels = vessels.withColumn("prev_latitude", lag("Latitude", 1).over(window_spec))
vessels = vessels.withColumn("prev_longitude", lag("Longitude", 1).over(window_spec))

# filter out null latitude/longitude rows
vessels = vessels.filter(col('prev_latitude').isNotNull() & col('prev_longitude').isNotNull()) \
                 .withColumn("dlon", radians(col("Longitude")) - radians(col("prev_longitude"))) \
                 .withColumn("dlat", radians(col("Latitude")) - radians(col("prev_latitude")))


# calculate the distance in km
radius = 6371
vessels = vessels.withColumn("distance_km", 2 * radius * asin(sqrt((1-cos(col("dlat")) + cos(radians(col("prev_latitude")))
                                                                    * cos(radians(col("Latitude"))) * (1-cos(col("dlon"))))/2)))
vessels.show(5)


# checking if there are outliers in distances based on sigma rule (or z-score) and filter them out
stats = vessels.select(
    mean(col("distance_km")).alias("mean"),
    stddev(col("distance_km")).alias("stddev")
).collect()

mean_distance = stats[0]['mean']
stddev_distance = stats[0]['stddev']

# calculate Z-score and filter
sigma = 3
vessels = vessels.withColumn("z_score", (col("distance_km") - mean_distance) / stddev_distance)
vessels = vessels.filter(abs(col("z_score")) <= 3)


# 2.2) aggregate by MMSI to get total distance per day of each vessel
total_distance_per_vessel = vessels.groupBy("MMSI").agg(sum("distance_km").alias("total_distance_km"))

# 3) sort to get top 5 vessels which travelled the most
top_k = 5
total_distance_per_vessel.sort("total_distance_km", ascending=False).show(top_k)

# based on our execution and outlier removal, vessel that traveled the most distance in km is:
# MMSI: 218795000 with total_distance_km: 1358.3675

spark.stop()




# COMMENTS
# ==================================================================
# We also tried udf approach but it did not work.
# udf in general take more time

# something is wrong with udf, does not work
# def haversine(lat1, lon1, lat2, lon2):
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     arg = sqrt((1 - cos(dlat) + cos(lat1) * cos(lat2) * (1 - cos(dlon)))/2)
#     radius = 6371  # radius of Earth in km
#     distance = 2*radius*asin(arg)
#     return distance
#
#
# # create udf
# haversine_udf = udf(haversine, FloatType())

# calculate the distance
# vessels = vessels.withColumn("distance_km", haversine(col("Latitude"), col("Longitude"), col("prev_latitude"), col("prev_longitude")))

