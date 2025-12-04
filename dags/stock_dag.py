from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.fetch_stock_data import fetch_and_store_stock_data

with DAG(
    dag_id='stock_data_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    fetch_ibm_stock_data = PythonOperator(
        task_id='fetch_ibm_stock_data',
        python_callable=fetch_and_store_stock_data,
        op_kwargs={'symbol': 'IBM'}
    )