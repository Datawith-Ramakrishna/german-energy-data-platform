
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="german_energy_pipeline",
    description="German electricity market data pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["energy", "data-engineering", "portfolio"],
) as dag:

    ingest_generation = BashOperator(
        task_id="ingest_generation",
        bash_command="cd /opt/airflow && python ingestion/load_generation.py",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "dbt build "
            "--project-dir /opt/airflow/energy_dbt "
            "--profiles-dir /opt/airflow/dbt"
        ),
    )

    ingest_generation >> dbt_build
