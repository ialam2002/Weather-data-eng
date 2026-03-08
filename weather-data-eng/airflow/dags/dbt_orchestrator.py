from datetime import datetime, timedelta
from docker.types import Mount
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'description': 'A DAG to orchestrate dbt runs',
    'start_date': datetime(2026, 3, 6),
    'catchup': False,
}

dag = DAG(
    dag_id='dbt_orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5),
)

with dag:
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