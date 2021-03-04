#!/bin/bash
spark-submit \
--master local \
--py-files /Users/muhid/Desktop/Springboard/guided-capstone-project/src/etl.zip \
ingestion.py 2020-01-02
&&
spark-submit \
--master local \
--py-files /Users/muhid/Desktop/Springboard/guided-capstone-project/src/etl.zip \
eod_load.py 2020-01-02 \
&&
spark-submit \
 --master local \
 --py-files /Users/muhid/Desktop/Springboard/guided-capstone-project/src/etl.zip \
analytical_etl.py 2020-01-02