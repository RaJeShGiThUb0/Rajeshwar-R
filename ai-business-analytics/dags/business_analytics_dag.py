"""Airflow/Cloud Composer orchestration DAG."""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="business_analytics_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "data-engineering", "bigquery"],
) as dag:
    ingest = BashOperator(
        task_id="ingest_csv",
        bash_command="python etl/ingest_csv.py",
    )
    transform = BashOperator(
        task_id="pyspark_transform",
        bash_command="python etl/transform_orders.py",
    )
    validate = BashOperator(
        task_id="data_quality_check",
        bash_command="python -m pytest tests -q",
    )

    ingest >> transform >> validate
