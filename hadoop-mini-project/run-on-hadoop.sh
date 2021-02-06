hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-*streaming*.jar \
-file src/autoinc_mapper1.py -mapper autoinc_mapper1.py \
-file src/autoinc_reducer1.py -reducer autoinc_reducer1.py \
-input input/data.csv -output output/all_accidents

hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-*streaming*.jar \
-file src/autoinc_mapper2.py -mapper autoinc_mapper2.py \
-file src/autoinc_reducer2.py -reducer autoinc_reducer2.py \
-input output/all_accidents -output output/make_year_count


