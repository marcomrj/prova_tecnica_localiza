from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
import logging


spark = SparkSession.builder \
    .appName("Top Sales Generator") \
    .getOrCreate()


def create_table():
    logging.info("Reading data from Delta Lake...")
    df = spark.read.format("delta").load("/root/output/etl_output")
    logging.info("Creating top sales table...")
    sales_df = df.filter(col("transaction_type") == "sale")

    windowSpec = Window.partitionBy("receiving_address")\
                       .orderBy(col("timestamp").desc())
    recent_sales_df = sales_df.withColumn("rn", row_number().over(windowSpec))\
                              .filter(col("rn") == 1).drop("rn")

    top_sales = recent_sales_df.orderBy(col("amount").desc()).limit(3)

    top_sales = top_sales.select("receiving_address", "amount", "timestamp")

    top_sales.write \
        .mode('overwrite') \
        .format('delta') \
        .save('/root/output/top_sales_table')
    logging.info("Top sales table created successfully!")
