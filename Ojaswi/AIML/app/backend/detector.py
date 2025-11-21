# app/backend/detector.py

from ultralytics import YOLO
import cv2
import numpy as np
import uuid
from datetime import datetime
import os

# Load your trained YOLO model
MODEL_PATH = "yolov8s.pt"
model = YOLO(MODEL_PATH)

def predict_image(img_path):
    """Run YOLO detection on a single image."""
    results = model.predict(img_path)[0]
    return results

def predict_frame(frame):
    """Run YOLO detection on webcam/video frame."""
    results = model.predict(frame, verbose=False)[0]
    return results

def save_violation(label, confidence, image):
    """Save detection logs in a folder."""
    os.makedirs("violations", exist_ok=True)

    file_id = str(uuid.uuid4())[:8]
    filename = f"violations/{file_id}.jpg"
    cv2.imwrite(filename, image)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"{file_id},{label},{confidence},{filename},{timestamp}\n"
    log_path = "violations_log.csv"

    with open(log_path, "a") as f:
        f.write(log_line)

    return filename, file_id, timestamp
