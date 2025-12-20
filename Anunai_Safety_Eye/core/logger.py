# core/logger.py
import os, csv
from datetime import datetime
import cv2

LOG_DIR = "logs"
SNAP_DIR = os.path.join(LOG_DIR, "violations")
CSV_PATH = os.path.join(LOG_DIR, "events.csv")

os.makedirs(SNAP_DIR, exist_ok=True)
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['timestamp', 'person_idx', 'event_type', 'missing_helmet', 'missing_vest', 'conf_summary', 'bbox', 'snapshot'])

def log_violation(person_idx, missing_helmet, missing_vest, conf_summary, bbox, frame):
    """
    Save snapshot and append CSV row.
    frame: BGR image (full frame). We'll crop person bbox for snapshot.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    x1,y1,x2,y2 = bbox
    # ensure bbox within image bounds
    h, w = frame.shape[:2]
    x1c = max(0, x1); y1c = max(0, y1); x2c = min(w, x2); y2c = min(h, y2)
    crop = frame[y1c:y2c, x1c:x2c] if (y2c>y1c and x2c>x1c) else frame
    snap_name = f"{ts}_p{person_idx}.jpg"
    snap_path = os.path.join(SNAP_DIR, snap_name)
    cv2.imwrite(snap_path, crop)
    # write csv row
    row = [ts, person_idx, 'violation', int(missing_helmet), int(missing_vest), conf_summary, str(bbox), snap_path]
    with open(CSV_PATH, 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow(row)
    return snap_path
