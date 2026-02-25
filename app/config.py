"""
Configuration module for DU University Chapters ETL pipeline.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ArcGIS FeatureService API URL
API_BASE_URL = (
    "https://services2.arcgis.com/5I7u4SJE1vUr79JC/"
    "arcgis/rest/services/UniversityChapters_Public/"
    "FeatureServer/0/query"
)

# Google Cloud configuration
GCP_PROJECT: str | None = os.getenv("GCP_PROJECT")
BQ_DATASET: str = os.getenv("BQ_DATASET", "du_data")
BQ_TABLE: str = os.getenv("BQ_TABLE", "university_chapters")

logging.info(
    "Configuration loaded: GCP_PROJECT=%s, BQ_DATASET=%s, BQ_TABLE=%s",
    GCP_PROJECT,
    BQ_DATASET,
    BQ_TABLE,
)