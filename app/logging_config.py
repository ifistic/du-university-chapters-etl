import logging
import os
from google.cloud import logging as cloud_logging

def setup_logging():
    """
    Configuring logs for both local and Google environments.
    """
    # creating log infor
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # If running in GCP environment, attach Cloud Logging handler
    if os.getenv("GOOGLE_CLOUD_PROJECT"):
        client = cloud_logging.Client()
        client.setup_logging()

    logging.info("Logging configured successfully.")

