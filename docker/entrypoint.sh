#!/bin/bash

# Atualiza o banco de dados do Airflow
airflow db upgrade

# Cria um usuário se não existir
if ! airflow users list | grep -q "admin"; then
    airflow users create \
        --username admin \
        --password admin \
        --firstname Anonymous \
        --lastname Admin \
        --role Admin \
        --email admin@example.com
fi

# O comando para iniciar depende do argumento passado para o entrypoint
if [ "$1" = "webserver" ]; then
    exec airflow webserver
elif [ "$1" = "scheduler" ]; then
    exec airflow scheduler
else
    exec "$@"
fi
