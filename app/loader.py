"""
Load module: Uploads transformed data into Google BigQuery.
"""

import logging
from typing import List, Dict, Any
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from app.config import GCP_PROJECT, BQ_DATASET, BQ_TABLE

def load_to_bigquery(chapters: List[Dict[str, Any]]) -> None:
    """
    Load transformed chapter records into BigQuery
    and logs the process.
    Raises:
    Exception: If insertion fails.
    """
    logging.info("LOAD | Starting BigQuery load process.")

    if not chapters:
        logging.warning("LOAD | No data provided. Skipping load.")
        return

    try:
        client = bigquery.Client(project=GCP_PROJECT)
        dataset_id = f"{GCP_PROJECT}.{BQ_DATASET}"
        table_id = f"{dataset_id}.{BQ_TABLE}"

        # Ensure dataset exists
        try:
            client.get_dataset(dataset_id)
            logging.info("LOAD | Dataset exists: %s", dataset_id)
        except NotFound:
            logging.info("LOAD | Creating dataset: %s", dataset_id)
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            client.create_dataset(dataset)

        # Ensure table exists or create it with the correct schema
        try:
            client.get_table(table_id)
            logging.info("LOAD | Table exists: %s", table_id)
        except NotFound:
            logging.info("LOAD | Creating table: %s", table_id)
            schema = [
                bigquery.SchemaField("chapter_id", "STRING"),
                bigquery.SchemaField("chapter_name", "STRING"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),
                bigquery.SchemaField("latitude", "FLOAT"),
                bigquery.SchemaField("longitude", "FLOAT"),
                bigquery.SchemaField("loaded_at", "TIMESTAMP"),
            ]
            table = bigquery.Table(table_id, schema=schema)
            client.create_table(table)
      
        # Insert rows into BigQuery and check for errors
        errors = client.insert_rows_json(table_id, chapters)
        if errors:
            logging.error("LOAD | Errors inserting rows: %s", errors)
            raise Exception(errors)

        logging.info(
            "LOAD | Successfully inserted %d rows into %s",
            len(chapters),
            table_id,
        )
        
    except Exception as exc:
        logging.critical("LOAD | BigQuery load failed: %s", exc, exc_info=True)
        raise