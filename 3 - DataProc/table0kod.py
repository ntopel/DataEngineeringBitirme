from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType, DecimalType

# Initialize Spark session
spark = SparkSession.builder.appName("KafkaToBigQuery").getOrCreate()
 
# Set your bucket and project configuration
bucket = "bucket_json02"
spark.conf.set("temporaryGcsBucket", bucket)
spark.conf.set("parentProject", "mindful-bivouac-395521")
# Define schema for JSON data
schema = StructType([
     StructField("adi", StringType()),
     StructField("bos", StringType()),
     StructField("dolu", StringType()),
     StructField("lon", StringType()),  
     StructField("lat", StringType()),  
     StructField("sonBaglanti", TimestampType())
 ])
# Read data from Kafka topic
kafkaDF = spark.readStream.format("kafka") \
     .option("kafka.bootstrap.servers", "34.125.130.154:9092") \
     .option("subscribe", "ornek") \
    .load()

# Parse JSON data and select fields
parsedDF = kafkaDF.selectExpr("CAST(value AS STRING)") \
     .select(from_json("value", schema).alias("parsed")) \
     .select("parsed.*")


# Convert columns to the appropriate data types
convertedDF = parsedDF.withColumn("bos", col("bos").cast(IntegerType())) \
                       .withColumn("dolu", col("dolu").cast(IntegerType())) \
                       .withColumn("lon", col("lon").cast(DecimalType(18, 9))) \
                       .withColumn("lat", col("lat").cast(DecimalType(18, 9)))

# Write data to BigQuery
query_bigquery = convertedDF.writeStream \
     .outputMode("append") \
     .format("bigquery") \
     .option("table", "db.table0") \
     .option("checkpointLocation", "/path/to/checkpoint/dir/in/hdfs") \
     .option("parentProject", "mindful-bivouac-395521") \
     .option("credentialsFile", "/home/nt110511/sw.json") \
     .start()

query_bigquery.awaitTermination()