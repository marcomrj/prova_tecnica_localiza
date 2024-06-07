from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, row_number
from pyspark.sql.window import Window



spark = SparkSession.builder \
    .appName("Google Drive CSV Reader") \
    .getOrCreate()

def create_table():
    # Lendo o arquivo Parquet
    df = spark.read.format("delta").load("/caminho/para/sua/tabela_delta")

    sales_df = df.filter(col("transaction_type") == "sale")

    # Usar Window para obter a transação mais recente por 'receiving address'
    windowSpec = Window.partitionBy("receiving_address").orderBy(col("timestamp").desc())
    recent_sales_df = sales_df.withColumn("rn", row_number().over(windowSpec)).filter(col("rn") == 1).drop("rn")

    # Ordenar por 'amount' em ordem decrescente e pegar os três primeiros
    top_sales = recent_sales_df.orderBy(col("amount").desc()).limit(3)

    # Selecionar colunas relevantes e mostrar o resultado
    top_sales = top_sales.select("receiving_address", "amount", "timestamp")

    # Sobrescrever os dados no mesmo local em formato Parquet
    top_sales.write \
    .mode('overwrite') \
    .format('delta') \
    .partitionBy("location_region") \
    .save('/root/output/etl_output')

                                                                         
    