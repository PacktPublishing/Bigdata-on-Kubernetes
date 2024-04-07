from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os

# set conf
conf = (
SparkConf()
    .set("spark.cores.max", "2")
        .set("spark.executor.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
        .set("spark.driver.extraJavaOptions", "-Dcom.amazonaws.services.s3.enableV4=true")
        .set("spark.hadoop.fs.s3a.fast.upload", True)
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .set("spark.hadoop.fs.s3a.aws.crendentials.provider", "com.amazonaws.auth.EnvironmentVariablesCredentials")
        .set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.3")
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()
    

if __name__ == "__main__":

    # init spark session
    spark = SparkSession\
            .builder\
            .appName("SparkApplicationJob")\
            .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark
        .read
        .format("csv")
        .options(header='true', inferSchema='true', delimiter=';')
        .load("s3a://<YOUR_BUCKET>/titanic.csv")
    )
    

    df.show()
    df.printSchema()

    (df
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3a://<YOUR_NEW_BUCKET>/titanic")
    )

    print("*****************")
    print("Successfully written!")
    print("*****************")

    spark.stop()
