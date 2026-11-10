
from pathlib import Path
import os

import pandas as pd
import psycopg
from dotenv import load_dotenv


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Actual_generation_202401010000_202402010000_Hour.csv"
)

load_dotenv(PROJECT_ROOT / ".env")


# --------------------------------------------------
# 2. Extract
# --------------------------------------------------

def extract_data():
    print("Reading SMARD electricity generation data...")

    df = pd.read_csv(
        CSV_FILE,
        sep=";",
        thousands=",",
        encoding="utf-8-sig",
        na_values=["-",""]
    )

    print(f"CSV rows: {len(df)}")
    print(f"CSV columns: {len(df.columns)}")

    return df


# --------------------------------------------------
# 3. Transform
# --------------------------------------------------

def transform_data(df):
    print("Transforming electricity generation data...")

    df["Start date"] = pd.to_datetime(
        df["Start date"],
        format="%b %d, %Y %I:%M %p",
    )

    df["End date"] = pd.to_datetime(
        df["End date"],
        format="%b %d, %Y %I:%M %p",
    )

    energy_columns = [
        col for col in df.columns
        if col not in ["Start date", "End date"]
    ]

    # Convert wide-format data into long-format data
    df_long = df.melt(
        id_vars=["Start date", "End date"],
        value_vars=energy_columns,
        var_name="energy_source",
        value_name="generation_mwh",
    )

    # Clean energy-source names
    df_long["energy_source"] = (
        df_long["energy_source"]
        .str.replace(
            " [MWh] Calculated resolutions",
            "",
            regex=False,
        )
        .str.strip()
    )

    df_long["generation_mwh"] = pd.to_numeric(
        df_long["generation_mwh"],
        errors="raise",
    )

    # Convert missing pandas values into Python None
    df_long["generation_mwh"] = df_long[
        "generation_mwh"
    ].astype(object).where(
        df_long["generation_mwh"].notna(),
        None,
    )

    print(f"Transformed observations: {len(df_long)}")

    return df_long


# --------------------------------------------------
# 4. Load
# --------------------------------------------------

def load_data(df):
    print("Connecting to PostgreSQL...")

    connection = psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )

    insert_query = """
        INSERT INTO raw.electricity_generation (
            interval_start,
            interval_end,
            energy_source,
            generation_mwh,
            source_file
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (
            interval_start,
            interval_end,
            energy_source
        )
        DO UPDATE SET
            generation_mwh = EXCLUDED.generation_mwh,
            source_file = EXCLUDED.source_file
        WHERE
            raw.electricity_generation.generation_mwh
                IS DISTINCT FROM EXCLUDED.generation_mwh
            OR
            raw.electricity_generation.source_file
                IS DISTINCT FROM EXCLUDED.source_file;
    """

    records = [
        (
            row[0].to_pydatetime(),
            row[1].to_pydatetime(),
            row[2],
            row[3],
            CSV_FILE.name,
        )
        for row in df[
            [
                "Start date",
                "End date",
                "energy_source",
                "generation_mwh",
            ]
        ].itertuples(index=False, name=None)
    ]

    with connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_query, records)

    print(f"Processed {len(records)} observations.")
    print("Database transaction committed successfully.")


# --------------------------------------------------
# 5. Pipeline
# --------------------------------------------------

def main():
    df = extract_data()
    df_transformed = transform_data(df)
    load_data(df_transformed)

    print("SMARD ingestion pipeline completed!")


if __name__ == "__main__":
    main()
