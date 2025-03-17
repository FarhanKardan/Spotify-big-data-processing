import os
from pyspark.sql import SparkSession

# Get HDFS address from environment variable or fallback
hdfs_address = os.getenv("HDFS_ADDRESS", "hdfs://172.18.0.3:9000")

print(f"Connecting to HDFS at: {hdfs_address}")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("WriteParquetToHDFS") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", hdfs_address) \
    .getOrCreate()

try:
    # Check if we can connect to HDFS
    hdfs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
    print("Successfully connected to HDFS.")
    
    root_path = spark._jvm.org.apache.hadoop.fs.Path(hdfs_address + "/")
    print(f"Listing files in: {hdfs_address}/")

    # List files and directories in HDFS root
    statuses = hdfs.listStatus(root_path)
    if statuses and len(statuses) > 0:
        print("Items found in HDFS root:")
        for status in statuses:
            path = status.getPath().toString()
            file_type = "Directory" if status.isDirectory() else "File"
            print(f"{file_type}: {path}")
    else:
        print("No files or directories found in HDFS root.")

except Exception as e:
    print(f"Error while accessing HDFS: {e}")
    e.printStackTrace()




# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, from_json, from_unixtime, date_format, hour
# from pyspark.sql.types import StructType, StructField, LongType, StringType, IntegerType, DoubleType

# # Initialize Spark session
# spark = SparkSession.builder \
#     .appName("KafkaToHDFSParquet") \
#     .master("spark://spark-master:7077") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
#     .config("spark.hadoop.ipc.maximum.data.length", "134217728") \
#     .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
#     .getOrCreate()

# spark.sparkContext.setLogLevel("INFO")  # Set log level to INFO for more detailed logs

# kafka_bootstrap_servers = "kafka:29092"

# # Kafka Stream Read
# kafka_df = spark.readStream.format("kafka") \
#     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#     .option("subscribe", "status_change_events") \
#     .option("startingOffsets", "earliest") \
#     .load()

# # Schema for the incoming status_change_events data
# status_change_event_schema = StructType([
#     StructField("ts", LongType(), True),
#     StructField("sessionId", IntegerType(), True),
#     StructField("page", StringType(), True),
#     StructField("auth", StringType(), True),
#     StructField("method", StringType(), True),
#     StructField("status", IntegerType(), True),
#     StructField("level", StringType(), True),
#     StructField("itemInSession", IntegerType(), True),
#     StructField("city", StringType(), True),
#     StructField("zip", StringType(), True),
#     StructField("state", StringType(), True),
#     StructField("userAgent", StringType(), True),
#     StructField("lon", DoubleType(), True),
#     StructField("lat", DoubleType(), True),
#     StructField("userId", IntegerType(), True),
#     StructField("lastName", StringType(), True),
#     StructField("firstName", StringType(), True),
#     StructField("gender", StringType(), True),
#     StructField("registration", LongType(), True)
# ])

# # Parse the Kafka data and apply the schema
# status_change_events_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
# parsed_df = status_change_events_df.select(from_json(col("json_str"), status_change_event_schema).alias("data")).select("data.*")

# # Add event time column based on timestamp
# processed_df = parsed_df.withColumn("event_time", from_unixtime((col("ts") / 1000).cast("long")).cast("timestamp"))
# processed_df = processed_df.withColumn("date", date_format(col("event_time"), "yyyy-MM-dd")) \
#                            .withColumn("hour", hour(col("event_time")))

# # Function to process and write each batch to HDFS
# def process_batch(batch_df, batch_id):
#     batch_df.write \
#         .format("parquet") \
#         .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/bronze/status_change_events") \
#         .option("path", "hdfs://namenode:9000/bronze/events/status_change_events") \
#         .mode("append") \
#         .save()

# # Write the processed data to Parquet in HDFS without partitioning
# query = processed_df.writeStream \
#     .outputMode("append") \
#     .foreachBatch(process_batch) \
#     .trigger(processingTime="1 minute") \
#     .start()

# query.awaitTermination()




# # from pyspark.sql import SparkSession
# # from pyspark.sql.functions import col, from_json
# # from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType

# # # Create a Spark session
# # spark = SparkSession.builder \
# #     .appName("SpotifyStreamProcessing") \
# #     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
# #     .getOrCreate()

# # # Define the schema of the incoming Kafka messages
# # schema = StructType([
# #     StructField("artist", StringType()),  
# #     StructField("song", StringType()),  
# #     StructField("duration", FloatType()),  # Adjusted to float
# #     StructField("ts", LongType()),  # Timestamp
# #     StructField("sessionId", LongType()),
# #     StructField("auth", StringType()),
# #     StructField("level", StringType()),
# #     StructField("itemInSession", LongType()),
# #     StructField("city", StringType()),
# #     StructField("zip", StringType()),
# #     StructField("state", StringType()),
# #     StructField("userAgent", StringType()),
# #     StructField("lon", FloatType()),  # Adjusted to float
# #     StructField("lat", FloatType()),  # Adjusted to float
# #     StructField("userId", LongType()),
# #     StructField("lastName", StringType()),
# #     StructField("firstName", StringType()),
# #     StructField("gender", StringType()),
# #     StructField("registration", LongType())
# # ])

# # # Read streaming data from Kafka
# # spotify_stream = spark.readStream \
# #     .format("kafka") \
# #     .option("kafka.bootstrap.servers", '127.0.0.1:9092') \
# #     .option("subscribe", 'listen_events') \
# #     .load()

# # # Convert the 'value' column (binary) to string using 'from_json' and apply the schema
# # processed_stream = spotify_stream.select(
# #     from_json(col("value").cast("string"), schema).alias("data")
# # ).select("data.*")  


# # def process_batch(df, epoch_id):
# #     print(f"Processing batch {epoch_id}")
# #     print(f"Number of rows in this batch: {df.count()}")
# #     df.show()  # Show the actual data

# # # Write the processed data to Parquet in HDFS without partitioning
# # query = processed_stream.writeStream \
# #     .outputMode("append") \
# #     .foreachBatch(process_batch) \
# #     .trigger(processingTime="1 minute") \
# #     .start()

# # query.awaitTermination()


