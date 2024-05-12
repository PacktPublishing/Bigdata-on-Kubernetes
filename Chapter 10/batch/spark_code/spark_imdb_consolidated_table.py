from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
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

    # Reading the tables from bronze zone
    names = spark.read.parquet("s3a://bdok-539445819060/bronze/imdb/names")
    basics = spark.read.parquet("s3a://bdok-539445819060/bronze/imdb/basics")
    crew = spark.read.parquet("s3a://bdok-539445819060/bronze/imdb/crew")
    principals = spark.read.parquet("s3a://bdok-539445819060/bronze/imdb/principals")
    ratings = spark.read.parquet("s3a://bdok-539445819060/bronze/imdb/ratings")

    # Exploding knownForTitles
    names = names.select(
        'nconst', 'primaryName', 'birthYear', 'deathYear', 
        f.explode(f.split('knownForTitles', ',')).alias('knownForTitles')
    )

    # Exploding directors in the crew table
    crew = crew.select(
        'tconst', f.explode(f.split('directors', ',')).alias('directors'), 'writers'
    )

    # Joining tables
    basics_ratings = basics.join(ratings, on=['tconst'], how='inner')
    principals_names = (
        principals.join(names, on=['nconst'], how='inner')
        .select('nconst', 'tconst','ordering', 'category', 'characters', 'primaryName', 'birthYear', 'deathYear')
        .dropDuplicates()
    )
    directors = (
        crew
        .join(names, on=crew.directors == names.nconst, how='inner')
        .selectExpr('tconst', 'directors', 'primaryName as directorPrimaryName', 
                    'birthYear as directorBirthYear', 'deathYear as directorDeathYear')
        .dropDuplicates()
    )

    basics_principals = basics_ratings.join(principals_names, on=['tconst'], how='inner').dropDuplicates()
    basics_principals_directors = basics_principals.join(directors, on=['tconst'], how='inner').dropDuplicates()

    # Write the results to silver zone
    basics_principals_directors.write.mode("overwrite").parquet("s3a://bdok-539445819060/silver/imdb/consolidated")

    spark.stop()
