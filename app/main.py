"""
Main ETL code that get data from fetche_chapters function,
cleans and return data to load_to_bigquery function to
load processed data to google cloud bigquery table and logs the process.
"""
import logging
#import pandas as pd
from datetime import datetime, timezone
from app.extractor import fetch_chapters
from app.loader import load_to_bigquery
#from google.cloud import bigquery
from app.config import GCP_PROJECT, BQ_DATASET, BQ_TABLE

from app.logging_config import setup_logging

setup_logging()

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s",
# )


def run_etl():
    logging.info("PIPELINE | ETL process started.")

    try:
        # Step 1: Extract
        chapters = fetch_chapters()
        if not chapters:
            logging.warning("PIPELINE | No chapters extracted. Skipping load.")
            return

        # Step 2: Transform
        for chapter in chapters:
            # Trim all string fields
            for key in ["chapter_id", "chapter_name", "city", "state"]:
                if chapter.get(key):
                    chapter[key] = chapter[key].strip()

            # Convert latitude/longitude to float
            chapter["latitude"] = float(chapter["latitude"]) if chapter["latitude"] else None
            chapter["longitude"] = float(chapter["longitude"]) if chapter["longitude"] else None

            # Add timezone-aware loaded_at timestamp
            chapter["loaded_at"] = datetime.now(timezone.utc).isoformat()
       
       

        # Step 3: Load into BigQuery
        load_to_bigquery(chapters)
        print(len(chapters))
        logging.info("PIPELINE | ETL process completed successfully.")

    except Exception as exc:
        logging.critical("PIPELINE | ETL failed: %s", exc, exc_info=True)
        raise


if __name__ == "__main__":
    
    try:
        run_etl()
    finally:
        # Flush and close all logging handlers to avoid CloudLoggingHandler shutdown warnings
        logging.shutdown()