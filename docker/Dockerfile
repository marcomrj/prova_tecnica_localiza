# Usamos uma imagem base do Python
FROM python:3.8-slim-buster

# Instala dependências do sistema para o Spark e JDK para o PySpark
RUN apt-get update && apt-get install -y \
    default-jdk \
    scala \
    git \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Define variáveis de ambiente para Java e Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Baixa e instala Apache Spark
RUN wget -q https://downloads.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz  -O /tmp/spark.tgz \
    && tar -xf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-3.4.3-bin-hadoop3 $SPARK_HOME \
    && rm /tmp/spark.tgz

# Instala dependências do sistema para o Spark e JDK para o PySpark
RUN apt-get update && apt-get install -y \
    default-jdk \
    scala \
    git \
    wget \
    vim \
    procps \
    && rm -rf /var/lib/apt/lists/*


# Instala Apache Airflow
RUN pip install apache-airflow==2.2.2 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.2/constraints-3.8.txt"

# Copia um script de inicialização (a ser criado)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Portas expostas
EXPOSE 8080 7077 6066

# Script de inicialização
ENTRYPOINT ["/entrypoint.sh"]
