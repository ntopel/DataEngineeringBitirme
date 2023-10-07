# DataEngineeringBitirme DataPipelineProject
İstanbul Data Science Academy Big Data & Data Engineering bootcamp sonu bitirme projem.


Table of Contents:


Prerequisites:

Data Ingestion with Apache NiFi

Data Streaming with Apache Kafka

Data Processing with Apache Spark

Data Warehousing with Google BigQuery

Data Analysis with DBT



Prerequisites

Java Development Kit (JDK) 8

Apache NiFi

Apache Kafka

Apache Spark

Google Cloud BigQuery

DBT



Installation

Java Development Kit (JDK) 8



Install OpenJDK 8:

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install openjdk-8-jdk



Apache NiFi

Download and extract Apache NiFi:

wget https://archive.apache.org/dist/nifi/1.13.2/nifi-1.13.2-bin.tar.gz

tar -xzvf nifi-1.13.2-bin.tar.gz

Start NiFi and import the provided template called isbike.xml.



Apache Kafka

Download and extract Apache Kafka:

wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.3.1.tgz

tar -xzvf kafka_2.12-3.3.1.tgz

cd kafka_2.12-3.3.1



Start Zookeeper and Kafka:

sudo nohup bin/zookeeper-server-start.sh config/zookeeper.properties &

sudo nohup bin/kafka-server-start.sh config/server.properties &



Create a Kafka topic:

sudo bin/kafka-topics.sh --create --topic ornek --bootstrap-server localhost:9092



Apache Spark

Run Spark Shell on Dataproc with the required packages and dependencies:

spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar


Google BigQuery

DBT

Install DBT as per its official documentation.

Data Ingestion with Apache NiFi

Configure NiFi to ingest data from the source.

Data Streaming with Apache Kafka

Start the Kafka producer and consumer.

Configure Kafka topics as needed.

Data Processing with Apache Spark

Use PySpark to process the data.

Clean and transform the data as required.

Data Warehousing with Google BigQuery

Load processed data into Google BigQuery tables.

Write SQL queries for data analysis.

Data Analysis with DBT

Create DBT models for data analysis.

Analyze bike station activity and generate insights.







