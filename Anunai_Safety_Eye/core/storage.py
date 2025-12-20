"""
core/storage.py

Small CSV-backed storage for logs. Schema is flexible:
Columns:
  timestamp, frame_id, people_count, violations_count, person_id, missing

- Frame summary row: person_id and missing empty, violations_count = N, people_count = M
- Violation rows: person_id and missing set (one row per violation), people_count repeated for context

Later: swap this to SQLite / Postgres (TODO: MIGRATE_TO_DB)
"""

import csv
import os
from typing import Dict, List

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "logs.csv")
FIELDNAMES = ["timestamp", "frame_id", "people_count", "violations_count", "person_id", "missing"]

def append_log(entry: Dict):
    """
    Append a dict entry to CSV. Keys should be among FIELDNAMES.
    """
    exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not exists:
            writer.writeheader()
        # make a safe row with default empty strings
        row = {k: entry.get(k, "") for k in FIELDNAMES}
        writer.writerow(row)

def read_logs(limit: int = 10000) -> List[Dict]:
    """
    Read up to `limit` rows from CSV. Returns list of dicts.
    """
    if not os.path.exists(CSV_PATH):
        return []
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader):
            rows.append(r)
            if i + 1 >= limit:
                break
    return rows
def clear_logs():
    """Delete logs.csv if it exists."""
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
