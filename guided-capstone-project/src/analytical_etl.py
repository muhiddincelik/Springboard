from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.window import *
import datetime
import findspark
import job_tracking
import sys

findspark.init()

# Get date argument from bash command
current_date = str(sys.argv[1])

# Create a job tracker instance
tracker = job_tracking.Tracker("analytical_etl", current_date)

# Applying try-except block for the whole script to track job status in MySQL
try:
    # Initialize a Spark session
    spark = SparkSession.builder.appName('Analytical ETL').getOrCreate()
    spark.conf.set("spark.sql.adaptive.enabled", "true")

    # define current date and previous date to use later
    current_datetime = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    previous_date = (current_datetime - datetime.timedelta(days=1)).date()


    # Read end-of-day trade data
    df = spark.read.parquet(f"../output/trade/trade_dt={current_date}")

    # Create a view of end-of-day trade dataframe
    df.createOrReplaceTempView("current_trade_data")

    # Calculate moving average trade price for last 30 minutes for each trade record
    current_mov_avg_df = spark.sql("""
                            SELECT 
                                symbol,
                                exchange,
                                event_tm,
                                event_seq_nb,
                                trade_pr,
                                AVG(trade_pr) OVER(PARTITION BY symbol ORDER BY event_tm
                                                   ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS mov_avg_pr 
                            FROM current_trade_data
                            """)

    # Create a view from moving averages dataframe
    current_mov_avg_df.write.saveAsTable("current_trade_moving_avg")


    # Read previous date's trade data and create a view from it
    prev_df = spark.read.parquet(f"../output/trade/trade_dt={previous_date}")
    prev_df.createOrReplaceTempView("previous_last_trade")

    # Select last moving average trade price from previous date's moving averages table
    previous_last_pr = spark.sql("""SELECT
                                    symbol,
                                    exchange,
                                    mov_avg_pr AS last_pr
                                    FROM
                                        (SELECT 
                                            symbol,
                                            exchange,
                                            event_tm,
                                            event_seq_nb,
                                            trade_pr,
                                            AVG(trade_pr) OVER(PARTITION BY symbol ORDER BY event_tm
                                                            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS mov_avg_pr, 
                                            RANK() OVER(PARTITION BY symbol ORDER BY event_tm DESC) AS rnk
                                        FROM previous_last_trade) prev
                                    WHERE prev.rnk = 1
                                    """)

    # Create a view from previous date's last moving average trade price table
    previous_last_pr.write.saveAsTable("previous_last_trade_pr")

    # Read current date's quote data and save it as a view
    quote_df = spark.read.parquet(f"../output/quote/quote_dt={current_date}")
    quote_df.write.saveAsTable("quote_table")

    # Union quote data with current_date's table of moving averages trade price
    quote_union_df = spark.sql("""
                                SELECT
                                    null AS trade_dt,
                                    "T" AS rec_type,
                                    symbol,
                                    exchange,
                                    event_tm,
                                    event_seq_nb,
                                    null AS bid_pr,
                                    null AS bid_size,
                                    null AS ask_pr,
                                    null AS ask_size,
                                    trade_pr,
                                    mov_avg_pr
                                FROM current_trade_moving_avg
                            UNION ALL
                                SELECT
                                    trade_dt,
                                    "Q" AS rec_type,
                                    symbol,
                                    exchange,
                                    event_tm,
                                    event_seq_nb,
                                    bid_pr,
                                    bid_size,
                                    ask_pr,
                                    ask_size,
                                    null AS trade_pr,
                                    null AS mov_avg_pr
                                FROM quote_table
                            """)

    # Save union dataframe as a view
    quote_union_df.createOrReplaceTempView("quote_union")

    # Populate the most recent trade price and moving average trade price into quote records for current date
    quote_union_update = spark.sql("""
                                SELECT
                                    trade_dt,
                                    rec_type,
                                    symbol,
                                    exchange,
                                    event_tm,
                                    event_seq_nb,
                                    bid_pr,
                                    bid_size,
                                    ask_pr,
                                    ask_size,
                                    MAX(last_trade_pr) OVER(PARTITION BY symbol) AS last_trade_pr,
                                    MAX(last_mov_pr) OVER(PARTITION BY symbol) AS last_mov_avg_pr
                                FROM
                                    (SELECT
                                        *,
                                        CASE WHEN rnk = 1 THEN trade_pr ELSE 0 END AS last_trade_pr,
                                        CASE WHEN rnk = 1 THEN mov_avg_pr ELSE 0 END AS last_mov_pr
                                    FROM
                                        (SELECT
                                            *,
                                            CASE WHEN trade_pr IS NULL THEN NULL
                                                ELSE RANK() OVER (PARTITION BY symbol ORDER BY
                                                                                        CASE WHEN trade_pr IS NULL THEN 1
                                                                                        ELSE 0 END, event_tm DESC)
                                            END AS rnk
                                        FROM quote_union))
                                  """)

    # Create a view for updated union
    quote_union_update.createOrReplaceTempView("quote_union_update")

    # Select required fields and filter by quote records.
    quote_update = spark.sql("""
                                SELECT
                                    trade_dt,
                                    symbol,
                                    event_tm,
                                    event_seq_nb,
                                    exchange,
                                    bid_pr,
                                    bid_size,
                                    ask_pr,
                                    ask_size,
                                    last_trade_pr,
                                    last_mov_avg_pr
                                FROM quote_union_update
                                WHERE rec_type = 'Q'
                            """)

    # Create a view from filtered quote dataframe
    quote_update.createOrReplaceTempView("quote_update")

    # Calculate bid price movement and ask price movement
    quote_final = spark.sql("""
                                SELECT
                                    trade_dt,
                                    symbol,
                                    event_tm,
                                    event_seq_nb,
                                    exchange,
                                    bid_pr,
                                    bid_size,
                                    ask_pr,
                                    ask_size,
                                    last_trade_pr,
                                    last_mov_avg_pr,
                                    bid_pr - last_pr as bid_pr_mv,
                                    ask_pr - last_pr as ask_pr_mv
                               FROM (
                                    SELECT /*+ BROADCAST(p) */
                                        q.*,
                                        p.last_pr
                                    FROM quote_update q LEFT OUTER JOIN previous_last_trade_pr p
                                        ON q.symbol = p.symbol AND q.exchange = p.exchange
                                    ) a
                            """)

    # Write finalized dataframe as parquet file
    quote_final.write.parquet(f"../output/quote-trade-analytical/date={current_date}")

    # Update job status accordingly in MySQL if there is no exception
    tracker.update_job_status("success")
except Exception as e:
    print(e)
    # Update job status accordingly in MySQL if there is exception
    tracker.update_job_status(f"failed")

