import os
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, CsvTableSink, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Rowtime, Json, Kafka, Elasticsearch
from pyflink.table.window import Tumble


def register_transactions_source(st_env):
    st_env.connect(Kafka()
                   .version("universal")
                   .topic("server-logs")
                   .start_from_earliest()
                   .property("zookeeper.connect", "host.docker.internal:2181")
                   .property("bootstrap.servers", "host.docker.internal:9092")) \
        .with_format(Json()
        .fail_on_missing_field(True)
        .schema(DataTypes.ROW([
        DataTypes.FIELD("event_id", DataTypes.STRING()),
        DataTypes.FIELD("account_id", DataTypes.DOUBLE()),
        DataTypes.FIELD("event_type", DataTypes.DOUBLE()),
        DataTypes.FIELD("location_country", DataTypes.DOUBLE()),
        DataTypes.FIELD("event_timestamp", DataTypes.TIMESTAMP(precision=3))]))) \
        .with_schema(Schema()
        .field("event_id", DataTypes.STRING())
        .field("account_id", DataTypes.DOUBLE())
        .field("event_type", DataTypes.STRING())
        .field("location_country", DataTypes.STRING())
        .field("event_timestamp", DataTypes.TIMESTAMP(precision=3))
        .field("row_time", DataTypes.TIMESTAMP(precision=3))
        .rowtime(
        Rowtime()
            .timestamps_from_field("event_timestamp")
            .watermarks_periodic_bounded(60000))) \
        .in_append_mode() \
        .create_temporary_table("source")


def register_transactions_es_sink(st_env):
    st_env.connect(Elasticsearch()
                   .version("7")
                   .host("0.0.0.0", 9200, "http")
                   .index("account-activity")
                   .document_type("usage")) \
        .with_schema(Schema()
                     .field("event_id", DataTypes.STRING())
                     .field("account_id", DataTypes.DOUBLE())
                     .field("event_type", DataTypes.STRING())
                     .field("location_country", DataTypes.STRING())
                     .field("event_timestamp", DataTypes.TIMESTAMP())
                     .field("row_time", DataTypes.TIMESTAMP())) \
        .with_format(Json().derive_schema()).in_upsert_mode().register_table_sink("sink_elasticsearch")


def activities_job():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_parallelism(1)
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

    st_env = StreamTableEnvironment \
        .create(s_env, environment_settings=EnvironmentSettings
                .new_instance()
                .in_streaming_mode()
                .use_blink_planner().build())

    st_env.get_config().get_configuration(). \
        set_string("pipeline.jars", "file:///C://Users//muhid//Downloads//flink-connector-kafka_2.12-1.12.1.jar;"
                                    "file:///C://Users//muhid//Downloads//flink-connector-elasticsearch_2.12-1.8.3.jar;")
    st_env.get_config().get_configuration(). \
        set_string("pipeline.classpaths", "file:///C://Users//muhid//Downloads//flink-connector-kafka_2.12-1.12.1.jar;"
                                          "file:///C://Users//muhid//Downloads//flink-connector-elasticsearch_2.12-1.8.3.jar")


    register_transactions_source(st_env)
    register_transactions_es_sink(st_env)

    st_env.from_path("source") \
        .window(Tumble.over("10.hours").on("row_time").alias("w")) \
        .group_by("location_country, w") \
        .select("""location_country as country, 
                   count(event_id) as count_events,
                   """) \
        .execute_insert("sink_elasticsearch", overwrite=True)

    st_env.execute_sql("app")


if __name__ == '__main__':
    activities_job()
