from airflow.models import DAG
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from plugins.operators.spark_operators import SparkScalaOperator, SparkPythonOperator
from airflow.utils.helpers import chain


with DAG(
    dag_id='first-dag',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    
    start = DummyOperator(task_id='start')
    spark_scala = SparkScalaOperator(
        task_id='spark-scala',
        class_name='com.example.SparkScalaJob',
    )
    spark_python = SparkPythonOperator(
        task_id='spark-python',
        pyfile='main.py'
    )
    end = DummyOperator(task_id='end')
    
    chain(start, [spark_scala, spark_python], end)