from processor import spark_processor as s
from pyspark.sql import SQLContext
from pyspark.sql.types import Row
from pyspark import sql
import datetime
import pytest

# Fixtures to use from conftest.py
pytest_mark = pytest.mark.usefixtures("spark_context", "sql_context")


def test_spark_transformation(spark_context, mocker):
    """ test that a single event is categorized correctly
    Args:
        spark_context: test fixture SparkContext
        sql_context: test fixture SqlContext
    """

    sqlContext = sql.SQLContext(spark_context)

    # Mocking the message coming from Kafka
    mocker.patch(
        'processor.spark_processor_refactored.read_from_kafka',
        return_value=spark_context.parallelize([Row(value='{"event_id": "141b3ff2a92111ebbfae367ddad5b1fa", '
                                                          '"account_id": "684", "event_type": "other", '
                                                          '"device": "ANDROID", "location_country": "FR", '
                                                          '"event_timestamp": "1619724510"}')]).toDF()
    )

    # Mocking the connection with MySQL
    mocker.patch(
        'processor.spark_processor_refactored.read_from_mysql',
        return_value=spark_context.parallelize([Row(account_no='684', user_device='ANDROID')]).toDF()
    )

    # Spark transformation result dataframe
    result = s.transform().collect()

    # Expected esult
    expected_result = [Row(event_id='141b3ff2a92111ebbfae367ddad5b1fa', account_id=684,
                           event_type='other', device='ANDROID', location_country='FR',
                           event_timestamp=datetime.datetime(2021, 4, 29, 12, 28, 30), status='good')]

    assert result == expected_result
