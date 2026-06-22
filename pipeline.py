"""
Pharma Sales Analytics Pipeline
================================
End-to-end Data Engineering pipeline:
Cloud Storage → Pandas ETL → BigQuery

Author: Priyanshu Pandita
GitHub: github.com/Priyanshupandita07
"""

import pandas as pd
import io
import logging
import sys
from google.cloud import storage, bigquery
from google.cloud.bigquery import LoadJobConfig, WriteDisposition

# ── LOGGING SETUP ─────────────────────────────────────────────
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ── CONFIG ────────────────────────────────────────────────────
PROJECT_ID   = "project-72181980-533d-4978-aa7"
BUCKET_NAME  = "de-practice-priyanshu"
RAW_FILE     = "raw/salesdaily.csv"
BQ_TABLE     = "de_practice.pharma_sales"
DRUG_COLS    = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]

# ── CLIENTS ───────────────────────────────────────────────────
client_bq  = bigquery.Client(project=PROJECT_ID)
client_gcs = storage.Client(project=PROJECT_ID)
bucket     = client_gcs.bucket(BUCKET_NAME)


# ── EXTRACT ───────────────────────────────────────────────────
def extract():
    """
    Download raw pharma sales CSV from Google Cloud Storage
    into a Pandas DataFrame.
    """
    logger.info("EXTRACT: Starting...")

    blob     = bucket.blob(RAW_FILE)
    raw_data = blob.download_as_text()
    df       = pd.read_csv(io.StringIO(raw_data))

    logger.info(f"EXTRACT: {len(df)} rows loaded from gs://{BUCKET_NAME}/{RAW_FILE} ✅")
    logger.info(f"EXTRACT: Columns — {list(df.columns)}")
    logger.info(f"EXTRACT: NULLs — {df.isna().sum().to_dict()}")

    return df


# ── TRANSFORM ─────────────────────────────────────────────────
def transform(df):
    """
    Clean and enrich the raw pharma sales data:
    - Convert datum to datetime
    - Add total_sales (sum of all drugs per day)
    - Add best_drug (top-selling drug per day)
    - Add is_weekend flag
    - Rename 'Weekday Name' to 'weekday_name'
    """
    logger.info("TRANSFORM: Starting...")

    # Convert datum to datetime
    df["datum"] = pd.to_datetime(df["datum"])
    logger.info("TRANSFORM: datum → datetime ✅")

    # Total daily sales across all drugs
    df["total_sales"] = df[DRUG_COLS].sum(axis=1)
    logger.info("TRANSFORM: total_sales column added ✅")

    # Best selling drug per day
    df["best_drug"] = df[DRUG_COLS].idxmax(axis=1)
    logger.info("TRANSFORM: best_drug column added ✅")

    # Weekend flag
    df["is_weekend"] = df["Weekday Name"].isin({"Saturday", "Sunday"})
    logger.info("TRANSFORM: is_weekend flag added ✅")

    # Rename column — remove space for BigQuery compatibility
    df = df.rename(columns={"Weekday Name": "weekday_name"})
    logger.info("TRANSFORM: 'Weekday Name' renamed to 'weekday_name' ✅")

    logger.info(f"TRANSFORM: {len(df)} clean rows ready ✅")
    return df


# ── LOAD ──────────────────────────────────────────────────────
def load(df):
    """
    Load clean DataFrame into BigQuery and verify with
    SQL analytics query.
    """
    logger.info("LOAD: Starting...")

    job_config = LoadJobConfig(
        write_disposition=WriteDisposition.WRITE_TRUNCATE
    )

    job = client_bq.load_table_from_dataframe(
        df,
        BQ_TABLE,
        job_config=job_config
    )
    job.result()

    logger.info(f"LOAD: {len(df)} rows written to {BQ_TABLE} ✅")

    # ── SQL ANALYTICS VERIFICATION ────────────────────────────
    query = f"""
        SELECT
            weekday_name,
            COUNT(*)                    AS total_days,
            ROUND(AVG(total_sales), 2)  AS avg_daily_sales
        FROM `{PROJECT_ID}.{BQ_TABLE}`
        GROUP BY weekday_name
        ORDER BY avg_daily_sales DESC
    """

    result = client_bq.query(query, location="asia-south1").to_dataframe()
    logger.info("LOAD: SQL verification complete ✅")

    print("\n📊 Average Pharma Sales by Day of Week:")
    print(result.to_string(index=False))


# ── RUN PIPELINE ──────────────────────────────────────────────
def run_pipeline():
    logger.info("=" * 50)
    logger.info("PHARMA SALES PIPELINE — STARTED")
    logger.info("=" * 50)

    raw   = extract()
    clean = transform(raw)
    load(clean)

    logger.info("=" * 50)
    logger.info("PHARMA SALES PIPELINE — COMPLETED ✅")
    logger.info("=" * 50)


if __name__ == "__main__":
    run_pipeline()
