from pyspark.sql import SparkSession
from pyspark.sql.types import *
import json_parser
import csv_parser
import findspark
import job_tracking
import sys

findspark.init()

# Get date argument from bash command
current_date = str(sys.argv[1])

# Create a job tracker instance
tracker = job_tracking.Tracker("initial_ingestion", current_date)

# Applying try-except block for the whole script to track job status in MySQL
try:
    spark = SparkSession.builder.appName('Data Ingestion').getOrCreate()
    spark.conf.set("spark.sql.adaptive.enabled", "true")

    # spark.conf.set (
    #     "fs.azure.account.key.<storage-account-name>.blob.core.windows.net",
    #     "<your-storage-account-access-key>"
    # )
    # raw = spark.textFile("wasbs://<container-name>@<storage-account-name>.blob.core.windows.net/<path_in_container>")

    # Create a common output schema to use when writing out the dataframes
    output_schema = StructType([StructField('trade_dt', DateType(), True),
                               StructField('rec_type', StringType(), True),
                               StructField('symbol', StringType(), True),
                               StructField('exchange', StringType(), True),
                               StructField('execution_id', StringType(), True),
                               StructField('event_tm', TimestampType(), True),
                               StructField('event_seq_nb', IntegerType(), True),
                               StructField('arrival_tm', TimestampType(), True),
                               StructField('trade_pr', DecimalType(7, 3), True),
                               StructField('trade_size', IntegerType(), True),
                               StructField('bid_pr', DecimalType(7, 3), True),
                               StructField('bid_size', IntegerType(), True),
                               StructField('ask_pr', DecimalType(7, 3), True),
                               StructField('ask_size', IntegerType(), True),
                               StructField('partition', StringType(), False),
                               StructField('bad_line', StringType(), True)])

    # Import csv file, parse it and write out with the partition on append mode.
    raw = spark.sparkContext.textFile(f"../data/{current_date}.csv")
    parsed_csv = raw.map(lambda line: csv_parser.parse_csv(line))
    csv_df = spark.createDataFrame(parsed_csv, schema=output_schema)
    csv_df.write.partitionBy("partition").mode("append").parquet(f"../output/{current_date}/")

    # Import json file, parse it and write out with the partition on append mode.
    raw = spark.sparkContext.textFile(f"../data/{current_date}.json")
    parsed_json = raw.map(lambda line: json_parser.parse_json(line))
    json_df = spark.createDataFrame(parsed_json, schema=output_schema)
    json_df.write.partitionBy("partition").mode("append").parquet(f"../output/{current_date}/")

    # Update job status accordingly in MySQL if there is no exception
    tracker.update_job_status("success")
except Exception as e:
    print(e)
    # Update job status accordingly in MySQL if there is exception
    tracker.update_job_status("failed")


