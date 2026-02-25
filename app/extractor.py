"""
Extraction module: Fetches chapter data from ArcGIS FeatureService
and extracts Chapter Id, Chapter Name, City, State, Latitude & Longitude,
all as strings, without skipping any features.
"""

import logging
import os
from typing import  List, Dict
import requests
from app.config import API_BASE_URL

MAX_RECORDS = int(os.getenv("MAX_RECORDS", 100))  # setting default records to  100 if not set

def fetch_chapters() -> List[Dict[str, str]]:
    """
    Fetch all chapters from  Ducks Unlimited University Chapters API 
    and extract these fields as strings and in a dictionary  form to 
    avod skipping any features:
    - chapter_id
    - chapter_name
    - city
    - state
    - latitude
    - longitude
    """
    logging.info("EXTRACT | Starting extraction from Ducks Unlimited University Chapters API .")
    all_chapters: List[Dict[str, str]] = []
    offset = 0

    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "outSR": "4326",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": MAX_RECORDS
        }

        try:
            response = requests.get(API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            features = data.get("features", [])

            if not features:
                logging.info("EXTRACT | No more features to fetch.")
                break

            for feature in features:
                attrs = feature.get("attributes", {})
                geom = feature.get("geometry", {})

                # Extract fields and convert all to strings (empty string if None)
                chapter_id = str(attrs.get("ChapterID") or "")
                chapter_name = str(attrs.get("University_Chapter") or "")
                city = str(attrs.get("City") or "")
                state = str(attrs.get("State") or "")
                latitude = str(geom.get("y") or "")
                longitude = str(geom.get("x") or "")

                all_chapters.append({
                    "chapter_id": chapter_id,
                    "chapter_name": chapter_name,
                    "city": city,
                    "state": state,
                    "latitude": latitude,
                    "longitude": longitude
                })
            
            # If fewer records than max, we've reached the end
            if len(features) < MAX_RECORDS:
                logging.info("EXTRACT | End of features in the API.")
                break

            offset += MAX_RECORDS

        except requests.RequestException as exc:
            logging.error(
                "EXTRACT | Failed to fetch chapters at offset %d: %s", offset, exc, exc_info=True
            )
            raise

    logging.info("EXTRACT | Extraction complete. Total chapters fetched from api: %d", len(all_chapters)) 
    #print(len(all_chapters))
    return all_chapters