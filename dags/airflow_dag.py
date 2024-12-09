from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from stream_to_kafka import start_streaming

start_date = datetime(2024, 11, 25, 12)

default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


with DAG(
    'random_users', 
    default_args=default_args, 
    schedule_interval='0 1 * * *',
    catchup=False
) as dag:
    stream_task = PythonOperator(
        task_id='write_data_stream_to_kafka',
        python_callable=start_streaming,
        dag=dag
    )

    stream_task