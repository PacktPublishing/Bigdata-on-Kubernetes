from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

conf = (
SparkConf()
    .set("spark.cores.max", "2")
        .set("spark.executor.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
        .set("spark.driver.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
        .set("spark.hadoop.fs.s3a.fast.upload", True)
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .set("spark.hadoop.fs.s3a.aws.crendentials.provider", "com.amazonaws.auth.EnvironmentVariablesCredentials")
        .set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.3,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()

if __name__ == "__main__":

    spark = (
        SparkSession.builder
        .appName("ConsumeFromKafka")
        .getOrCreate()
    ) 

    spark.sparkContext.setLogLevel('ERROR') 

    df = ( 
        spark.readStream 
        .format('kafka') 
        .option("kafka.bootstrap.servers", "kafka-cluster-kafka-bootstrap:9092") 
        .option("subscribe", "src-customers")
        .option("startingOffsets", "earliest") 
        .load() 
    )

    schema1 = StructType([
        StructField("schema", StringType(), False),
        StructField("payload", StringType(), False)
    ])

    schema2 = StructType([
        StructField("name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("email", StringType(), False),
        StructField("photo", StringType(), False),
        StructField("birthdate", StringType(), False),
        StructField("profession", StringType(), False),
        StructField("dt_update", LongType(), False)
    ])

    o = df.selectExpr("CAST(value AS STRING)")

    o2 = o.select(f.from_json(f.col("value"), schema1).alias("data")).selectExpr("data.payload")
    o2 = o2.selectExpr("CAST(payload AS STRING)")
    newdf = o2.select(f.from_json(f.col("payload"), schema2).alias("data")).selectExpr("data.*")

    query = (
        newdf
        .withColumn("dt_birthdate", f.col("birthdate"))
        .withColumn("today", f.to_date(f.current_timestamp() ) )
        .withColumn("age", f.round(
            f.datediff(f.col("today"), f.col("dt_birthdate"))/365.25, 0)
        )
        .select("name", "gender", "birthdate", "profession", "age", "dt_update")
    )
    write_schema = '{"schema":{"type":"struct","fields":[{"type":"string","optional":true,"field":"name"},{"type":"string","optional":true,"field":"gender"},{"type":"string","optional":true,"field":"birthdate"},{"type":"string","optional":true,"field":"profession"},{"type":"int64","optional":true,"field":"age"},{"type":"int64","optional":true,"name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"dt_update"}],"optional":false},"payload":'

    json_query = (
        query
        .select(
            f.to_json(f.struct(f.col("*")))
        )
        .toDF("value")
    )

    (
        json_query
        .withColumn("value", f.concat(f.lit(write_schema), f.col("value"), f.lit('}')))
        .selectExpr("CAST(value AS STRING)")
        .writeStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka-cluster-kafka-bootstrap:9092")
        .option("topic", "customers-transformed")
        .option("checkpointLocation", "s3a://bdok-<ACCOUNT-NUMBER>/spark-checkpoint/customers-processing/")
        .start()
        .awaitTermination()
    )
