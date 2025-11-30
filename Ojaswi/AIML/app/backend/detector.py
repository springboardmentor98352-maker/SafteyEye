# app/backend/detector.py

from ultralytics import YOLO
import cv2
import numpy as np
import uuid
from datetime import datetime
import os

# Load your trained YOLO model
MODEL_PATH = "model/yolov8s.pt"   # change to "best.pt" if needed
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
    """Save violation image and log details."""
    
    # ensure folders exist
    os.makedirs("violations", exist_ok=True)
    os.makedirs("database", exist_ok=True)

    # create unique file name
    file_id = str(uuid.uuid4())[:8]
    filename = f"violations/{file_id}.jpg"

    # save image
    cv2.imwrite(filename, image)

    # timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # log file path
    log_path = os.path.join("database", "violations_log.csv")

    # data entry format
    log_line = f"{file_id},{label},{confidence},{filename},{timestamp}\n"

    # write to log file
    with open(log_path, "a") as f:
        f.write(log_line)

    return filename, file_id, timestamp
