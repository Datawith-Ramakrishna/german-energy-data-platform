
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

with psycopg.connect(
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
) as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT current_database(), current_user"
        )
        database, user = cursor.fetchone()

        print(f"Connected to database: {database}")
        print(f"Connected as user: {user}")
