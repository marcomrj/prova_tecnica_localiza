#!/bin/bash

# Inicializa o scheduler do Airflow em background
airflow db init
airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.com
airflow webserver -p 8082 &

# Inicia o master e worker do Spark
start-master.sh -p 7077
start-worker.sh spark://localhost:7077

# Mantém o container rodando
tail -f /dev/null
