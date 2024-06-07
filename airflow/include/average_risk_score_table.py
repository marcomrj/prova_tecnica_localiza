from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg



spark = SparkSession.builder \
    .appName("Google Drive CSV Reader") \
    .getOrCreate()

def create_table():
    df = spark.read.format("delta").load("/caminho/para/sua/tabela_delta")

    average_risk_score = df.groupBy("location_region") \
                       .agg(avg("risk_score").alias("average_risk_score")) \
                       .orderBy(col("average_risk_score").desc())

    average_risk_score.write \
    .mode('overwrite') \
    .format('delta') \
    .partitionBy("location_region") \
    .save('/root/output/etl_output')
