FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    default-jdk \
    scala \
    git \
    wget \
    vim \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN wget -q https://downloads.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz  -O /tmp/spark.tgz \
    && tar -xf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-3.4.3-bin-hadoop3 $SPARK_HOME \
    && rm /tmp/spark.tgz

RUN apt-get update && apt-get install -y \
    default-jdk \
    scala \
    git \
    wget \
    vim \
    procps \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2
RUN pip install apache-airflow[cncf.kubernetes] virtualenv
RUN pip install apache-airflow==2.9.1 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.1/constraints-3.8.txt"
RUN pip install pyspark gdown
RUN mkdir -p /root/data_source

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080 7077 6066

ENTRYPOINT ["/entrypoint.sh"]
