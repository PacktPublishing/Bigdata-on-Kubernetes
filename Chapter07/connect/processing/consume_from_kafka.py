from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
    .appName("ConsumeFromKafka")
    .getOrCreate()
) 

spark.sparkContext.setLogLevel('ERROR') 

df = ( 
    spark.readStream 
    .format('kafka') 
    .option("kafka.bootstrap.servers", "localhost:9092") 
    .option("subscribe", "json-customers") 
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
    .groupBy("gender")
    .agg(
        f.count(f.lit(1)).alias("count"),
        f.first("dt_birthdate").alias("first_birthdate"),
        f.first("today").alias("first_now"),
        f.round(f.avg("age"), 2).alias("avg_age")
    )
)

(
    query
    .writeStream
    .format("console")
    .outputMode("complete")
    .start()
    .awaitTermination()
)
