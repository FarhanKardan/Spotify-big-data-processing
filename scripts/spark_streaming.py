from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, from_unixtime, date_format, hour
from pyspark.sql.types import StructType, StructField, LongType, StringType, DoubleType, BooleanType, IntegerType


spark = SparkSession.builder \
    .appName("KafkaToHDFSParquet") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")\
    .config("spark.hadoop.ipc.maximum.data.length", "134217728")\
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000")\
    .getOrCreate() 
    
spark.sparkContext.setLogLevel("WARN")

kafka_bootstrap_servers = "kafka:29092"


#========================================================Status Change Events===================================================

kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "status_change_events") \
    .option("startingOffsets", "earliest") \
    .load()

status_change_event_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("page", StringType(), True),
    StructField("auth", StringType(), True),
    StructField("method", StringType(), True),
    StructField("status", IntegerType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", StringType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DoubleType(), True),
    StructField("lat", DoubleType(), True),
    StructField("userId", IntegerType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True)
])

status_change_events_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = status_change_events_df.select(from_json(col("json_str"), status_change_event_schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("event_time", from_unixtime((col("ts") / 1000).cast("long")).cast("timestamp"))
processed_df = processed_df.withColumn("date", date_format(col("event_time"), "yyyy-MM-dd")) \
                           .withColumn("hour", hour(col("event_time")))

repartitioned_df = processed_df.repartition("date", "hour")

status_change_events_stream = repartitioned_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/bronze/status_change_events") \
    .option("path", "hdfs://namenode:9000/bronze/events/status_change_events") \
    .partitionBy("date", "hour") \
    .trigger(processingTime="1 minute") \
    .outputMode("append") \
    .start()

#========================================================Page View Events===================================================
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "page_view_events") \
    .option("startingOffsets", "earliest") \
    .load()

page_view_event_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("page", StringType(), True),
    StructField("auth", StringType(), True),
    StructField("method", StringType(), True),
    StructField("status", IntegerType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", StringType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DoubleType(), True),
    StructField("lat", DoubleType(), True),
    StructField("userId", IntegerType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True)
])

page_view_events_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = page_view_events_df.select(from_json(col("json_str"), page_view_event_schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("event_time", from_unixtime((col("ts") / 1000).cast("long")).cast("timestamp"))
processed_df = processed_df.withColumn("date", date_format(col("event_time"), "yyyy-MM-dd")) \
                           .withColumn("hour", hour(col("event_time")))

repartitioned_df = processed_df.repartition("date", "hour")

page_view_events_stream = repartitioned_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/bronze/page_view_events") \
    .option("path", "hdfs://namenode:9000/bronze/events/page_view_event") \
    .partitionBy("date", "hour") \
    .trigger(processingTime="1 minute") \
    .outputMode("append") \
    .start()


#========================================================Auth Events===================================================
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "auth_events") \
    .option("startingOffsets", "earliest") \
    .load()

auth_event_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", StringType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DoubleType(), True),
    StructField("lat", DoubleType(), True),
    StructField("userId", IntegerType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True),
    StructField("success", BooleanType(), True)
])

auth_events_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = auth_events_df.select(from_json(col("json_str"), auth_event_schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("event_time", from_unixtime((col("ts") / 1000).cast("long")).cast("timestamp"))
processed_df = processed_df.withColumn("date", date_format(col("event_time"), "yyyy-MM-dd")) \
                           .withColumn("hour", hour(col("event_time")))

repartitioned_df = processed_df.repartition("date", "hour")

auth_events_stream = repartitioned_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/bronze/auth_events") \
    .option("path", "hdfs://namenode:9000/bronze/events/auth_events") \
    .partitionBy("date", "hour") \
    .trigger(processingTime="1 minute") \
    .outputMode("append") \
    .start()

#========================================================Listen Events==================================================
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", "listen_events") \
    .option("startingOffsets", "earliest") \
    .load()

listen_event_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", LongType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", StringType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DoubleType(), True),
    StructField("lat", DoubleType(), True),
    StructField("userId", LongType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True),
    StructField("success", BooleanType(), True),
    StructField("artist", StringType(), True),
    StructField("song", StringType(), True),
    StructField("duration", DoubleType(), True),
    StructField("auth", StringType(), True),
    StructField("page", StringType(), True),
    StructField("method", StringType(), True),
    StructField("status", IntegerType(), True)
])

listen_events_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")
parsed_df = listen_events_df.select(from_json(col("json_str"), listen_event_schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("event_time", from_unixtime((col("ts") / 1000).cast("long")).cast("timestamp"))
processed_df = processed_df.withColumn("date", date_format(col("event_time"), "yyyy-MM-dd")) \
                           .withColumn("hour", hour(col("event_time")))

repartitioned_df = processed_df.repartition("date", "hour")

listent_event_stream = repartitioned_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/bronze/listen_events") \
    .option("path", "hdfs://namenode:9000/bronze/events/listen_events") \
    .partitionBy("date", "hour") \
    .trigger(processingTime="1 minute") \
    .outputMode("append") \
    .start()



status_change_events_stream.awaitTermination()
page_view_events_stream.awaitTermination()
auth_events_stream.awaitTermination()
listent_event_stream.awaitTermination()