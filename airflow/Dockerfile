
FROM apache/airflow:3.1.3-python3.12

USER airflow

RUN pip install --no-cache-dir \
    "dbt-core==1.10.15" \
    "dbt-postgres==1.10.0" \
    pandas \
    "psycopg[binary]" \
    python-dotenv
