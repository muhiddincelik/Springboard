import logging
import pytest

from pyspark import HiveContext
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark import SQLContext
from pyspark.streaming import StreamingContext
from pyspark import sql

def quiet_py4j():
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_context(request):
    conf = (SparkConf().setMaster("local[2]").setAppName("pytest-pyspark-local-testing"))
    request.addfinalizer(lambda: sc.stop())

    sc = SparkContext(conf=conf)
    quiet_py4j()
    return sc


@pytest.fixture(scope="session")
def hive_context(spark_context):
    return HiveContext(spark_context)


@pytest.fixture(scope="session")
def sql_context(spark_context):
    sql_context = sql.SQLContext(spark_context)
    return sql_context


@pytest.fixture(scope="session")
def streaming_context(spark_context):
    return StreamingContext(spark_context, 1)
