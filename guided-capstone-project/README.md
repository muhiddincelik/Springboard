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
I have created another function to parse the json file line by line and enforce the expected data types and check the event_type values. If a line(row) doesn't fit to the expected profile it is marked as bad record("B") in the partition field. Here I have assumed that each json record has all field names as in the common schema but may not have values depending on the type of the event. You can look into the [json_parser.py](src/json_parser.py) here in detail.

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
1) **Q**: Quote Record
2) **T**: Trade Record
3) **B**: Bad Record Regardless of the Event Type

Output directory looks like:

<kbd> <img src="images/output.jpg" /> </kbd>

## STEP 3: END-OF-DAY (EOD) DATA LOAD
Now that we’ve preprocessed the incoming data from the exchange, we need to create the final data format to store.

#### 1) Read Trade and Quote Partition Dataset From Their Temporary Location ####

		trade_common = spark.read.parquet("../output/partition=T")
		
		quote_common = spark.read.parquet("../output/partition=Q")
		
#### 2) Select The Necessary Columns For Trade and Quote Dataframes ###

		trade_df = trade_common.select("trade_dt", "symbol", "exchange", "execution_id", "event_tm", "event_seq_nb",
                               "arrival_tm", "trade_pr", "trade_size")
		
		quote_df = quote_common.select("trade_dt", "symbol", "exchange", "event_tm", "event_seq_nb",
                               "arrival_tm", "bid_pr", "bid_size", "ask_pr", "ask_size")
							   
#### 3) Create Window Specs and Apply Them to Retrieve the Records With The Latest Arrival Time ####

		trade_window = Window.partitionBy(col("trade_dt"), col("symbol"), col("exchange"), col("event_tm"), col("event_seq_nb"),
                                col("execution_id")).orderBy(col("arrival_tm").desc())
		
		trade_df = trade_df.withColumn("row_number", row_number().over(trade_window))
		
		trade_df = trade_df.where(col("row_number") == 1).drop(col("row_number")) 		# Drop the unnecessary row_number column 
								
		quote_window = Window.partitionBy(col("trade_dt"), col("symbol"), col("exchange"), col("event_tm"), col("event_seq_nb"))\
                   .orderBy(col("arrival_tm").desc())
				   
		quote_df = quote_df.withColumn("row_number", row_number().over(quote_window))
		
		quote_df = quote_df.where(col("row_number") == 1).drop(col("row_number"))
		
#### 4) Write Out The Dataframes ####

		# Define a EOD date to use when writing Trade and Quote dataframes
		eod_date = d.today().date()
		
		# Write the cleaned Quote dataframe as parquet file
		trade_df.write.parquet("../output/trade/trade_dt={}" .format(eod_date))
		
		# Write the cleaned Quote dataframe as parquet file
		quote_df.write.parquet("../output/quote/quote_dt={}".format(eod_date))
		
		
		
	