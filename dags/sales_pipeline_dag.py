import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow/project")


def run_sales_pipeline():
    import os

    os.chdir("/opt/airflow/project")
    from src.main import main

    main()

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["sales"],
) as dag:
    PythonOperator(task_id="run_pipeline", python_callable=run_sales_pipeline)