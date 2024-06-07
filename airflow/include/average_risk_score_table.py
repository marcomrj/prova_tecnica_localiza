from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
import logging


spark = SparkSession.builder \
    .appName("Average Risk Score Generator") \
    .getOrCreate()


def create_table():
    logging.info("Reading data from Delta Lake...")
    df = spark.read.format("delta").load("/root/output/etl_output")

    logging.info("Creating average risk score table...")
    average_risk_score = df.groupBy("location_region") \
        .agg(avg("risk_score").alias("average_risk_score")) \
        .orderBy(col("average_risk_score").desc())

    average_risk_score.write \
        .mode('overwrite') \
        .format('delta') \
        .partitionBy("location_region") \
        .save('/root/output/average_risk_score_table')
    logging.info("Top sales table created successfully!")
