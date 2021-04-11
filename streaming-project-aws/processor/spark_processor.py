from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import KafkaConsumer
import mysql_connect_class
from generator.server_log_generator import ServerLogGenerator
import findspark

# Utilize find spark in case mysql package not found
findspark.add_packages('mysql:mysql-connector-java:8.0.11')

# Set Kafka config
# kafka_broker_hostname = 'broker'
# kafka_consumer_port = '9092'
# kafka_broker = kafka_broker_hostname + ':' + kafka_consumer_port
kafka_broker = "b-2.log.02msna.c8.kafka.us-west-2.amazonaws.com:9092," \
               "b-1.log.02msna.c8.kafka.us-west-2.amazonaws.com:9092"
kafka_topic_input = "server-logs"

# MySQL Connection Parameters
mysql_host = 'stream-database.cp2rkjojtqyn.us-west-2.rds.amazonaws.com'
mysql_port = '3306'

if __name__ == "__main__":
    # Create Spark session
    spark = SparkSession\
        .builder\
        .appName("CategorizeServerLogs")\
        .getOrCreate()

    # Spark session configurations
    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.sql.session.timeZone", "PST")
#    spark.sparkContext.addPyFile("mysql_con.py.zip")
    spark.conf.set("spark.sql.streaming.checkpointLocation", "./checkpoint")

    # Create a connection instance and call methods
    m = mysql_connect_class.MySQLPython()
    m.get_db_connection()
    m.create_table()
    m.create_dim_table()

    # Create a ServerLogGenerator instance to get predefined values
    s = ServerLogGenerator()

    countries = s._location_country  # Pre-defined countries
    event_types = s._event_type      # Pre-defined events
    devices = ["ANDROID", "IOS"]    # Pre-defined devices

    # Consume server logs from Kafka topic
    # consumer = KafkaConsumer(kafka_topic_input)
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_broker) \
        .option("subscribe", kafka_topic_input) \
        .option("includeHeaders", "true") \
        .load()

    # Convert message bytes from Kafka broker into String type
    df1 = df.selectExpr("CAST(value AS STRING) as value")

    # Define the schema to read JSON formatted data
    log_schema = StructType() \
        .add("event_id", StringType()) \
        .add("account_id", StringType()) \
        .add("event_type", StringType()) \
        .add("device", StringType()) \
        .add("location_country", StringType()) \
        .add("event_timestamp", StringType())

    # Parse JSON data and apply the schema
    df2 = df1.select(from_json(df1.value, schema=log_schema).alias("log_data"))

    # Select columns with alias
    df3 = df2.select(
        col("log_data.event_id").alias("event_id"),
        col("log_data.account_id").alias("account_id"),
        col("log_data.event_type").alias("event_type"),
        col("log_data.device").alias("device"),
        col("log_data.location_country").alias("location_country"),
        col("log_data.event_timestamp").alias("event_timestamp"))

    # Read users dimensional data from MySql to use in join
    df_dim_users = spark.read.format("jdbc").options(
        url=f'jdbc:mysql://{mysql_host}:{mysql_port}/dim_users',
        driver="com.mysql.cj.jdbc.Driver",
        dbtable="users",
        user="root",
        password="root1234").load()

    # Mutate df_dim_users by renaming  columns to avoid ambiguity during join
    df_dim_users = df_dim_users.withColumn('account_id', col('account_id').cast(StringType())) \
        .withColumnRenamed('account_id', 'account_no')\
        .withColumnRenamed('device', 'user_device')

    # Join dimensional users data with streaming dataframe
    df3 = df3.join(broadcast(df_dim_users), expr('account_id = account_no AND device = user_device'), "left_outer")\
        .select(col("event_id"),
                col("account_id"),
                col("event_type"),
                col("device"),
                col("user_device").alias('original_device'),
                col("location_country"),
                col("event_timestamp"))

    # Column variable for 'status' column with conditions
    status_col = when((length(df3.event_id) != 32) |
                      (isnull(df3.account_id.cast(IntegerType()))) |
                      ((~isnull(df3.account_id.cast(IntegerType()))) & (df3.account_id.cast(IntegerType()) > 10000)) |
                      (length(df3.event_timestamp) < 10) |
                      (df3.event_timestamp.contains('-')) |
                      (~df3.location_country.isin(countries)) |
                      (~df3.event_type.isin(event_types)) |
                      (~df3.device.isin(devices)) |
                      (isnull(df3.event_id)) |
                      (isnull(df3.account_id)) |
                      (isnull(df3.event_type)) |
                      (isnull(df3.device)) |
                      (isnull(df3.location_country)) |
                      (isnull(df3.event_timestamp)), "bad") \
        .when((isnull(df3.original_device)), 'suspicious') \
        .otherwise("good")

    # Mutate df3 with adding status column
    df3 = df3.withColumn("status", status_col)

    # Convert timestamps with '0' values to null to avoid errors
    timestamp_column = when(df3.event_timestamp == "0", None).otherwise(df3.event_timestamp)

    # Create a final dataframe by converting account_id into int and event timestamp into timestamp data types
    df_final = df3.withColumn('account_id', df3['account_id'].cast(IntegerType())) \
        .withColumn('event_timestamp', to_timestamp(timestamp_column.cast(IntegerType())))

    # We can drop original device column since we created status column already
    df_final = df_final.drop(col('original_device'))

    # Declare jdbc properties
    db_target_properties = {"user": "root", "password": "root1234", "driver": 'com.mysql.cj.jdbc.Driver'}

    # Create a function to use in foreachBatch
    def process_batch(batch_df, batch_id):
        batch_df.persist()  # Cache batch_df to avoid duplicate reads for each batch

        # Write "good" logs to the MySql table we created by calling create_table on MySQLPython instance
        batch_df.filter(batch_df.status == "good").write.jdbc(url=f'jdbc:mysql://{mysql_host}:{mysql_port}/logs',
                                                              table="good_logs",
                                                              mode="append",
                                                              properties=db_target_properties)

        # Write "bad" logs to the MySql table we created by calling create_table on MySQLPython instance
        batch_df.filter(batch_df.status == "bad").write.jdbc(url=f'jdbc:mysql://{mysql_host}:{mysql_port}/logs',
                                                             table="bad_logs",
                                                             mode="append",
                                                             properties=db_target_properties)

        # Write "suspicious" logs to the MySql table we created by calling create_table on MySQLPython instance
        batch_df.filter(batch_df.status == "suspicious").write.jdbc(url=f'jdbc:mysql://{mysql_host}:{mysql_port}/logs',
                                                                    table="suspicious_logs",
                                                                    mode="append",
                                                                    properties=db_target_properties)

        # Write categorized logs into a Kafka topic
        (batch_df.select(to_json(struct([batch_df[x] for x in batch_df.columns])).alias("value"))
            .write
            .format("kafka")
            .option("kafka.bootstrap.servers", kafka_broker)
            .option("topic", "server-logs-status")
            .save())

        batch_df.unpersist()  # Un-cache the batch_df after we write everything

    # Query to write out defined dataframes in process_batch function
    writer = df_final.writeStream.foreachBatch(process_batch).start()

    spark.streams.awaitAnyTermination()

