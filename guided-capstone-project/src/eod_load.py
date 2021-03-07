from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import *
from datetime import datetime as d
import job_tracking
import sys

# Get date argument from bash command
current_date = str(sys.argv[1])

# Create a job tracker instance
tracker = job_tracking.Tracker("eod_load", current_date)

# Applying try-except block for the whole script to track job status in MySQL
try:
    spark = SparkSession.builder.appName('Data Ingestion').getOrCreate()
    spark.conf.set("spark.sql.adaptive.enabled", "true")

    # END OF DAY LOAD FOR TRADE DATA

    # Read Trade Partition Data
    trade_common = spark.read.parquet(f"../output/{current_date}/partition=T")

    # Select relevant columns from the common schema
    trade_df = trade_common.select("trade_dt", "symbol", "exchange", "execution_id", "event_tm", "event_seq_nb",
                                   "arrival_tm", "trade_pr", "trade_size")

    # Create a window spec to inspect the most recent record if there are multiple records per composite key fields
    trade_window = Window.partitionBy(col("trade_dt"), col("symbol"), col("exchange"), col("event_tm"), col("event_seq_nb"),
                                    col("execution_id")).orderBy(col("arrival_tm").desc())

    # Apply the window with row_number function
    trade_df = trade_df.withColumn("row_number", row_number().over(trade_window))

    # Select the records where row_number 1 (latest arrival_time) and drop row_number column
    trade_df = trade_df.where(col("row_number") == 1).drop(col("row_number"))

    # Define a EOD date to use when writing Trade and Quote data

    # Write the cleaned Quote data as parquet file
    trade_df.write.parquet(f"../output/trade/trade_dt={current_date}")

    # END OF DAY LOAD FOR QUOTE DATA

    # Read Quote Partition Data
    quote_common = spark.read.parquet(f"../output/{current_date}/partition=Q")

    # Select relevant columns from the common schema
    quote_df = quote_common.select("trade_dt", "symbol", "exchange", "event_tm", "event_seq_nb",
                                   "arrival_tm", "bid_pr", "bid_size", "ask_pr", "ask_size")

    # Create a window spec to inspect the most recent record if there are multiple records per composite key fields
    quote_window = Window.partitionBy(col("trade_dt"), col("symbol"), col("exchange"), col("event_tm"), col("event_seq_nb"))\
                       .orderBy(col("arrival_tm").desc())

    # Apply the window with row_number function
    quote_df = quote_df.withColumn("row_number", row_number().over(quote_window))

    # Select the records where row_number 1 (latest arrival_time) and drop row_number column
    quote_df = quote_df.where(col("row_number") == 1).drop(col("row_number"))

    # Write the cleaned Quote data as parquet file
    quote_df.write.parquet(f"../output/quote/quote_dt={current_date}")

    # Update job status accordingly in MySQL if there is no exception
    tracker.update_job_status("success")
except Exception as e:
    print(e)
    # Update job status accordingly in MySQL if there is exception
    tracker.update_job_status("failed")

