import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import sys
sys.path.append('/opt/airflow/api-requests')
from insert_records import main
from airflow.providers.docker.operators.docker import DockerOperator
default_args = {
    'description': 'Orchestrator DAG for Weather API data pipeline',
    'start_date': '2024-03-06',
    'catchup': False,
}

dag = DAG(
    dag_id='weather-api-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=1),
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data',
        python_callable=main,
    )
    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[Mount(source='weather-data-eng/dbt/my_project', target='/usr/app', type='bind'),
                Mount(source='weather-data-eng/dbt/profiles.yml',target='/root/.dbt/profiles.yml',type='bind')],
        network_mode='weather-data-eng_my_network',
        docker_url='unix:///var/run/docker.sock',
        auto_remove='success',
    )

    task1 >> task2