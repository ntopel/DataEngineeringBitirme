Scala

# Write credentials key file
nano sw.json 

-------------------------------------------------------------------------------------------------------------

spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar

-------------------------------------------------------------------------------------------------------------

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
-----------------------------------------------------------------------------------------------------------------










import spark.implicits._

import org.apache.spark.sql.types._

import org.apache.spark.sql.functions

import java.sql.Timestamp

import org.apache.spark.sql.streaming.Trigger.ProcessingTime

val bucket = "idsaproje1"

spark.conf.set("temporaryGcsBucket", bucket)

spark.conf.set("parentProject", "mineral-rune-365815")

val kafkaDF = spark.readStream.format("kafka").option("kafka.bootstrap.servers","34.170.27.9:9092").option("subscribe","ornek").load

val schema = StructType(List(StructField("name",StringType),StructField("country",StringType),StructField("localtime",StringType),StructField("temp_c",FloatType)))
val activationDF = kafkaDF.select(from_json($"value".cast("string"),schema).alias("activation"))
val modelCountDF = activationDF.groupBy($"activation"("name"),$"activation"("country"),$"activation"("localtime"),$"activation"("temp_c")).count.sort($"count".desc)


val modelCountQuery = modelCountDF.writeStream.outputMode("complete").format("bigquery").option("table","idsadb.idsadb_table").option("checkpointLocation", "/path/to/checkpoint/dir/in/hdfs").option("credentialsFile","/home/isteveriseti1/mineral.json").option("failOnDataLoss",false).option("truncate",false).start().awaitTermination()
