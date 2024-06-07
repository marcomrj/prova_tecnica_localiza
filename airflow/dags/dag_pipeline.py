from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from etl import run
from average_risk_score_table import create_table as avarage_risk_score
from top_sales_table import create_table as top_sales

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'pipeline_dag',
    default_args=default_args,
    description='ETL pipeline using Apache Spark and Delta Lake',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=run,
    dag=dag,
    )

    avarage_risk_score_task = PythonOperator(
        task_id='avarage_risk_score',
        python_callable=avarage_risk_score,
        dag=dag,
    )

    top_sales_task = PythonOperator(
        task_id='top_sales',
        python_callable=top_sales,
        dag=dag,
    )

    end = DummyOperator(
        task_id='end'
    )

    start >> run_etl >> [avarage_risk_score_task,top_sales_task] >> end
