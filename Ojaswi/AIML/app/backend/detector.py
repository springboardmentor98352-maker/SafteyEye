# app/backend/detector.py

# app/backend/detector.py

from ultralytics import YOLO
import cv2
import uuid
from datetime import datetime
import os

# --------------------------------------------------
# Load YOLO Model
# --------------------------------------------------
MODEL_PATH = "model/yolov8s.pt"   # change to best.pt if trained
model = YOLO(MODEL_PATH)


def predict_image(img_path):
    """Run YOLO detection on a single image."""
    return model.predict(img_path)[0]


def predict_frame(frame):
    """Run YOLO detection on webcam/video frame."""
    return model.predict(frame, verbose=False)[0]


def count_people(results):
    """
    Count number of persons detected in a frame.
    Uses YOLO 'person' class.
    """
    count = 0
    for det in results.boxes:
        cls_name = results.names[int(det.cls[0])]
        if cls_name.lower() == "person":
            count += 1
    return count


def save_violation(label, confidence, image):
    """Save violation image and log details."""

    os.makedirs("violations", exist_ok=True)
    os.makedirs("database", exist_ok=True)

    file_id = str(uuid.uuid4())[:8]
    filename = f"violations/{file_id}.jpg"

    cv2.imwrite(filename, image)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_path = os.path.join("database", "violations_log.csv")
    log_line = f"{file_id},{label},{confidence},{filename},{timestamp}\n"

    with open(log_path, "a") as f:
        f.write(log_line)

    return filename, file_id, timestamp

