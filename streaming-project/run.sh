#!/bin/bash

python ./generator/server_log_class.py && \
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 --py-files ./processor/mysql_connect_class.py.zip ./processor/spark_processor.py
