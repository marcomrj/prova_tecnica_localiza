from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import when, lower, col
from functools import reduce
import gdown
import os
import logging


spark = SparkSession.builder \
    .appName("Data Processing with Delta Lake") \
    .config("spark.sql.shuffle.partitions", "500") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()


def run():
    df = _extract()
    df_transformed = _transform(df)
    _load(df_transformed)

def remove_non_textual(df: DataFrame, column: str) -> DataFrame:
    pattern = "^[A-Za-z\\s_,.]+$"
    df_filtered = df.filter(col(column).rlike(pattern))
    return df_filtered


def _extract():
    logging.info("Downloading data from Google Drive...")
    url = 'https://drive.google.com/uc?id=1Vumu8jo3P3umuUtBZb6mn7YoVIo4X0ON'
    local_file_path = "/root/data_source/df_fraud_credit.csv"
    gdown.download(url, local_file_path, quiet=False)
    logging.info("Reaging data as DataFrame...")
    df = spark.read.csv(local_file_path, header=True, inferSchema=True)
    return df


def _transform(df):
    logging.info("Transforming data...")
    df_transformed = df.withColumn("location_region",
                                   when(df["location_region"] == "South",
                                        "South America")
                                   .when(df["location_region"] == "North",
                                         "North America")
                                   .otherwise(df["location_region"]))\
        .withColumn("ip_prefix",
                    when(df["ip_prefix"] == "America", df["login_frequency"])
                    .otherwise(df["ip_prefix"]))\
        .withColumn("login_frequency",
                    when(col("login_frequency").contains("."),
                         col("session_duration"))
                    .otherwise(col("login_frequency")))\
        .withColumn("session_duration",
                    when(df["purchase_pattern"].cast("int").isNull(),
                         df["purchase_pattern"])
                    .otherwise(df["session_duration"]))\
        .withColumn("purchase_pattern",
                    when(df["purchase_pattern"].cast("int").isNull(),
                         df["age_group"])
                    .otherwise(df["purchase_pattern"]))\
        .withColumn("age_group",
                    when((col("age_group") != "veteran") &
                         (col("age_group") != "new") &
                         (col("age_group") != "established"),
                         col("risk_score"))
                    .otherwise(col("age_group")))\
        .withColumn("risk_score",
                    when(df["anomaly"].contains("."), df["anomaly"])
                    .otherwise(df["risk_score"]))\
        .withColumn("anomaly",
                    when(col("risk_score") < 60.0, "low_risk")
                    .when(col("risk_score") >= 90.0, "high_risk")
                    .otherwise("moderate_risk"))\
        .dropna()\
        .filter(~reduce(lambda a, b: a | b, (lower(col(c)) == 'none'
                                             for c in df.columns)))
    
    df_transformed = remove_non_textual(df_transformed, "location_region")
    df_transformed = remove_non_textual(df_transformed, "anomaly")
    df_transformed = remove_non_textual(df_transformed, "age_group")
    df_transformed = remove_non_textual(df_transformed, "purchase_pattern")
    df_transformed = remove_non_textual(df_transformed, "transaction_type")

    return df_transformed


def _load(df):
    logging.info("Saving data as Delta Lake...")
    df.write \
        .mode('overwrite') \
        .format('delta') \
        .partitionBy("location_region") \
        .save('/root/output/etl_output')
    logging.info("Data saved successfully!")
    os.remove('/root/data_source/df_fraud_credit.csv')
