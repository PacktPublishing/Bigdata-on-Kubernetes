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

    # Define Schemas
    schema_names = "nconst string, primaryName string, birthYear int, deathYear int, primaryProfession string, knownForTitles string"
    schema_basics = """
    tconst string, titleType string, primaryTitle string, originalTitle string, isAdult int, startYear int, endYear int,
    runtimeMinutes double, genres string
    """
    schema_crew = "tconst string, directors string, writers string"
    schema_principals = "tconst string, ordering int, nconst string, category string, job string, characters string"
    schema_ratings = "tconst string, averageRating double, numVotes int"

    # Read tables from S3 in TSV format
    names = (
        spark
        .read
        .schema(schema_names)
        .options(header=True, delimiter="\t")
        .csv('s3a://bdok-539445819060/landing/imdb/names.tsv.gz')
    )

    basics = (
        spark
        .read
        .schema(schema_basics)
        .options(header=True, delimiter="\t")
        .csv('s3a://bdok-539445819060/landing/imdb/basics.tsv.gz')
    )

    crew = (
        spark
        .read
        .schema(schema_crew)
        .options(header=True, delimiter="\t")
        .csv('s3a://bdok-539445819060/landing/imdb/crew.tsv.gz')
    )

    principals = (
        spark
        .read
        .schema(schema_principals)
        .options(header=True, delimiter="\t")
        .csv('s3a://bdok-539445819060/landing/imdb/principals.tsv.gz')
    )

    ratings = (
        spark
        .read
        .schema(schema_ratings)
        .options(header=True, delimiter="\t")
        .csv('s3a://bdok-539445819060/landing/imdb/ratings.tsv.gz')
    )

    # Write tables in S3 in parquet
    names.write.mode("overwrite").parquet("s3a://bdok-539445819060/bronze/imdb/names")
    basics.write.mode("overwrite").parquet("s3a://bdok-539445819060/bronze/imdb/basics")
    crew.write.mode("overwrite").parquet("s3a://bdok-539445819060/bronze/imdb/crew")
    principals.write.mode("overwrite").parquet("s3a://bdok-539445819060/bronze/imdb/principals")
    ratings.write.mode("overwrite").parquet("s3a://bdok-539445819060/bronze/imdb/ratings")

    spark.stop()