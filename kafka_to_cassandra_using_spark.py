import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType
from pyspark.sql.functions import from_json, col

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("spark_streaming")


def initialize_spark_session():
    try:
        spark = SparkSession.builder \
                .appName('SparkStreaming') \
                .config('spark.jars.packages',  "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0, org.apache.spark:spark-sql-kafka-0-10_2.13-3.5.3") \
                .config('spark.cassandra.connection.host', 'cassandra') \
                .config("spark.cassandra.connection.port","9042")\
                .config("spark.cassandra.auth.username", "cassandra") \
                .config("spark.cassandra.auth.password", "cassandra") \
                .getOrCreate()
        
        spark.sparkContext.setLogLevel("ERROR")

        logging.info('Spark session created successfully')
    except Exception:
        logging.error("ERROR: Couldn't initialize the spark session")
    
    return spark


def read_from_kafka_topic(spark, topic):
    try:
        df = spark.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', "kafka1:19092,kafka2:19093,kafka3:19094") \
            .option("subscribe", topic) \
            .option("delimeter",",") \
            .option("startingOffsets", "earliest") \
            .load()
        logging.info("Initial dataframe from Kafka topic created successfully")
    except Exception as e:
        logging.warning(f"Initial dataframe couldn't be created due to exception: {e}")
        return None
    
    return df


def process_dataframe(df):
    schema = StructType([
        StructField('full_name', StringType(), False),
        StructField('email', StringType(), False),
        StructField('contact_number', StringType(), False),
        StructField('username', StringType(), False),
        StructField('password', StringType(), False),
        StructField('date_of_birth', StringType(), False),
        StructField('age', StringType(), False),
        StructField('gender', StringType(), False),
        StructField('street_address', StringType(), False),
        StructField('city', StringType(), False),
        StructField('state', StringType(), False),
        StructField('country', StringType(), False),
        StructField('postcode', StringType(), False)
    ])

    df = df.selectExpr("CAST(value AS STRING)").select(from_json(col('value'), schema).alias('data')).select('data.*')

    return df


def start_streaming(df):
    logging.info('Spark Streaming is being started...')

    query = (df.writeStream \
            .format('org.apache.spark.sql.cassandra') \
            .outputMode('append') \
            .options(table='users', keyspace='social_network') \
            .option("checkpointLocation", "/mnt/checkpoints") \
            .start())
    
    return query.awaitTermination()


def write_stream_to_cassandra():
    spark = initialize_spark_session()
    df = read_from_kafka_topic(spark, 'random_users')
    if not df:
        logging.info('Kafka Topic has no new messages. Aborting stream write to Cassandra...')
    else:
        data = process_dataframe(df)
        start_streaming(data)


if __name__ == '__main__':
    write_stream_to_cassandra()
