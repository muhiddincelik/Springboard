# EQUITY MARKET DATA ANALYSIS

![equity_market](assets/equity_market.jpg)

## STEP 1: ETL DESIGN

![design](assets/guided-pipeline-design.jpg)

## STEP 2: DATA INGESTION

#### OUTPUT SCHEMA
I have defined the 'partition' field as non-nullable whereas others as nullable in the main script([ingestion.py](src/ingestion.py)). This is due to the fact that for 'bad' records we report all fields as null except 'partition' and 'bad_line' fields.

		# Create a common output schema to apply when writing out the dataframes
		output_schema = StructType([StructField('trade_dt', DateType(), False),
								   StructField('rec_type', StringType(), False),
								   StructField('symbol', StringType(), False),
								   StructField('exchange', StringType(), False),
								   StructField('execution_id', StringType(), True),
								   StructField('event_tm', TimestampType(), False),
								   StructField('event_seq_nb', IntegerType(), False),
								   StructField('arrival_tm', TimestampType(), False),
								   StructField('trade_pr', DecimalType(7, 3), True),
								   StructField('trade_size', IntegerType(), True),
								   StructField('bid_pr', DecimalType(7, 3), True),
								   StructField('bid_size', IntegerType(), True),
								   StructField('ask_pr', DecimalType(7, 3), True),
								   StructField('ask_size', IntegerType(), True),
								   StructField('partition', StringType(), False),
								   StructField('bad_line', StringType(), True)])
	
#### PARSING CSV FILE
I have created a function to parse the csv file line by line and enforce the expected data types and check the event_type values. If a line(row) doesn't fit to the expected profile it is marked as bad record("B") in the partition field. You can look into the [csv_parser.py](src/csv_parser.py) here in detail.

#### PARSING JSON FILE
I have created another function to parse the json file line by line and enforce the expected data types and check the event_type values. If a line(row) doesn't fit to the expected profile it is marked as bad record("B") in the partition field. Here I have assumed that each json record has all field names as in the common schema but may not have values depending on the type of the event. You can look into the [json_parser.py]here (src/json_parser.py) in detail.

#### DATA INGESTION FRAMEWORK
We read the both csv and json input files as text files. We call the parsing functions inside the map function before converting them into dataframes.

Ingest csv data:

		# Import csv file, parse it and write out with the partition on append mode.
		raw = spark.sparkContext.textFile("../data/data.csv")
		parsed_csv = raw.map(lambda line: csv_parser.parse_csv(line))
		csv_df = spark.createDataFrame(parsed_csv, schema=output_schema)
		csv_df.write.partitionBy("partition").mode("append").csv("../output/")

Ingest json data:

		# Import json file, parse it and write out with the partition on append mode.
		raw = spark.sparkContext.textFile("../data/data.json")
		parsed_json = raw.map(lambda line: json_parser.parse_json(line))
		json_df = spark.createDataFrame(parsed_json, schema=output_schema)
		json_df.write.partitionBy("partition").mode("append").csv("../output/")


As you can see above, we write out the dataframes by enabling partition based on 'partition' column.

**Partition field** possible values:
1) **E**: Exchange Record
2) **T**: Trade Record
3) **B**: Bad Record Regardless of the Event Type

Output directory looks like:

<kbd> <img src="images/output.jpg" /> </kbd>


