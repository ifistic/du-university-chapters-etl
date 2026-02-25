import pandas as pd
from app.extractor import fetch_chapters

EXPECTED_ROWS = 136
ALLOWED_DEVIATION = 20


def test_row_count_drift():
    chapters = fetch_chapters()
    df = pd.DataFrame(chapters)

    row_count = len(df)

    assert abs(row_count - EXPECTED_ROWS) <= ALLOWED_DEVIATION, (
        f"Row count drift detected. Expected ~{EXPECTED_ROWS}, got {row_count}"
    )
