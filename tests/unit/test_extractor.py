# tests/unit/test_extractor.py

import pytest
from unittest.mock import patch, Mock
from app.extractor import fetch_chapters

# Sample fake response from ArcGIS
FAKE_RESPONSE = {
    "features": [
        {
            "attributes": {
                "ChapterID": "FL-0110",
                "University_Chapter": "Florida State University",
                "City": "Tallahassee",
                "State": "FL"
            },
            "geometry": {
                "x": -84.304272637,
                "y": 30.438110943
            }
        },
        {
            "attributes": {
                "ChapterID": "CA-0220",
                "University_Chapter": "Stanford University",
                "City": "Stanford",
                "State": "CA"
            },
            "geometry": {
                "x": -122.1687,
                "y": 37.4275
            }
        }
    ]
}


@patch("app.extractor.requests.get")
def test_fetch_chapters_all_fields(mock_get):
    """
    Test fetch_chapters to ensure:
    - All expected keys exist
    - No row has missing or empty values
    """
    # Arrange: mock requests.get to return our fake response
    mock_response = Mock()
    mock_response.json.return_value = FAKE_RESPONSE
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # Act: call the extractor
    chapters = fetch_chapters()

    # Assert: correct number of rows
    assert len(chapters) == 2

    # Assert: all keys exist and values are non-empty strings
    required_keys = ["chapter_id", "chapter_name", "city", "state", "latitude", "longitude"]
    for chapter in chapters:
        for key in required_keys:
            assert key in chapter, f"Missing key {key}"
            assert chapter[key] != "", f"Empty value for key {key} in chapter {chapter}"