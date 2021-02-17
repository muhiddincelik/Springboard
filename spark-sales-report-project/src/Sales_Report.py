import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *


spark = SparkSession.builder.appName('Sales Report').getOrCreate()
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Creating a schema
schema = StructType([
    StructField("incident_id",IntegerType(),True),
    StructField("incident_type",StringType(),True),
    StructField("vin",StringType(),True),
    StructField("make", StringType(), True),
    StructField("model", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("incident_date", StringType(), True),
    StructField("description", StringType(), True)
])


# Importing csv file with the schema above
sales = spark.read.format('csv') \
    .option("header", False) \
    .option("sep", ',') \
    .schema(schema) \
    .load("data/data.csv")

"""
Extract make and model info per vin group using Window and filter the rows with the incident_type 'A' and
select only make and model columns.
"""
windowSpec = Window.partitionBy("vin").orderBy("vin")
sales = sales.withColumn("make2", max("make").over(windowSpec)) \
             .withColumn("year2", max("year").over(windowSpec)) \
             .filter(col("incident_type") == 'A') \
             .select(col('make2').alias('make'), col('year2').alias('year'))

"""
Apply mapping to convert each row into tuple(make-year, 1), then apply reduceByKey to aggregate the count
per make-year pair. Then we convert rdd to dataframe and write it as csv file. 
"""
report_df = sales.rdd.map(lambda x: tuple([x["make"] + '-' + str(x["year"]), 1]))\
                     .reduceByKey(lambda x, y: x+y)\
                     .toDF(('Make_Model', 'Count'))\
                     .write.csv("output/Sales_Report.csv")



