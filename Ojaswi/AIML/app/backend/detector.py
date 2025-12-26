from ultralytics import YOLO
import cv2
import uuid
from datetime import datetime
import os
import csv
from pathlib import Path

# --------------------------------------------------
# Load YOLO Model
# --------------------------------------------------
MODEL_PATH = "model/yolov8s.pt"
model = YOLO(MODEL_PATH)

# --------------------------------------------------
# Paths
# --------------------------------------------------
DB_DIR = Path("database")
LOG_PATH = DB_DIR / "violations_log.csv"
IMG_DIR = Path("violations")

DB_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Ensure CSV exists with proper header
# --------------------------------------------------
if not LOG_PATH.exists():
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label", "confidence", "image", "timestamp"])


# --------------------------------------------------
# YOLO Prediction
# --------------------------------------------------
def predict_frame(frame):
    return model.predict(frame, verbose=False)[0]


# --------------------------------------------------
# Count People
# --------------------------------------------------
def count_people(results):
    count = 0
    for det in results.boxes:
        cls_name = results.names[int(det.cls[0])]
        if cls_name.lower() == "person":
            count += 1
    return count


# --------------------------------------------------
# SAFE LABEL NORMALIZATION (VERY IMPORTANT)
# --------------------------------------------------
def normalize_label(label: str) -> str:
    # CSV-safe label (no commas)
    return label.replace(",", " /")


# --------------------------------------------------
# Save Violation (SAFE + APPEND MODE)
# --------------------------------------------------
def save_violation(label, confidence, image):

    file_id = str(uuid.uuid4())[:8]
    img_path = IMG_DIR / f"{file_id}.jpg"
    cv2.imwrite(str(img_path), image)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_label = normalize_label(label)

    # 🔒 Append safely (NO pandas, NO read)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([
            file_id,
            safe_label,
            round(float(confidence), 4),
            str(img_path),
            timestamp
        ])

    return str(img_path), file_id, timestamp


# --------------------------------------------------
# Delete Violation (Image + PDF + CSV row)
# --------------------------------------------------
def delete_violation(vid):

    if not LOG_PATH.exists():
        return False

    rows = []
    deleted = False

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == vid:
                img = Path(row[3])
                pdf = DB_DIR / f"{vid}.pdf"

                if img.exists():
                    img.unlink()
                if pdf.exists():
                    pdf.unlink()

                deleted = True
            else:
                rows.append(row)

    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(rows)

    return deleted
