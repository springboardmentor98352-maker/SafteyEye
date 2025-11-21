"""
core/inference.py

Unified inference API. Current implementation: simulator for demo.
When you have a trained YOLOv8 model, replace the simulate_* functions
or implement load_model() and run_inference(image) to return the same format.

Return format (for frames):
  frame_rgb, detections

detections: list of dicts, each:
  {
    "person_id": int or None,       # local tracking id (simulated)
    "bbox": (x1, y1, x2, y2),       # pixel coords in frame
    "missing": ["helmet","vest"]    # list of missing PPE strings (empty if correct)
  }
"""

import random
import cv2
import numpy as np

def simulate_frame(frame_id: int, people_count: int = 3, violation_rate: float = 20.0, show_boxes: bool = True):
    """
    Create a synthetic frame and detections for demo purposes.

    Args:
        frame_id: int, used to build simple deterministic placement
        people_count: how many people to draw
        violation_rate: percent chance per person to have any violation
        show_boxes: draw bounding boxes

    Returns:
        (frame_rgb, detections)
    """
    h, w = 480, 720
    frame = np.ones((h, w, 3), dtype=np.uint8) * 200
    detections = []

    for i in range(people_count):
        # simple arrangement to avoid overlap and give consistent visuals
        x1 = int((i + 0.1) * w / (people_count + 1)) - 30
        y1 = 150 + ((i * 7) % 80)  # slight vertical variation
        x2 = x1 + 60
        y2 = y1 + 150
        x1, x2 = max(5, x1), min(w - 5, x2)

        # decide violations
        missing = []
        if random.random() < violation_rate / 100.0:
            missing = random.choice([["helmet"], ["vest"], ["helmet", "vest"]])

        # draw person (body + head)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), -1)
        cv2.circle(frame, (int((x1 + x2) / 2), y1 - 18), 16, (120, 160, 200), -1)

        # helmet indicator
        if "helmet" not in missing:
            cv2.rectangle(frame, (x1, y1 - 40), (x2, y1 - 22), (0, 200, 0), -1)
        else:
            cv2.rectangle(frame, (x1, y1 - 40), (x2, y1 - 22), (0, 0, 200), 2)

        # vest indicator
        if "vest" not in missing:
            cv2.rectangle(frame, (x1 + 6, y1 + 30), (x2 - 6, y1 + 90), (0, 200, 0), -1)
        else:
            cv2.rectangle(frame, (x1 + 6, y1 + 30), (x2 - 6, y1 + 90), (0, 0, 200), 2)

        detections.append({
            "person_id": i,
            "bbox": (x1, y1, x2, y2),
            "missing": missing
        })

        if show_boxes:
            color = (0, 200, 0) if not missing else (0, 0, 200)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"P{i}", (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, detections


# -----------------------------
# TODO: REPLACE_WITH_YOLOv8
# How to replace:
# - Implement load_model(path) that returns a cached model object
# - Implement run_inference(model, frame_bgr/ndarray) that returns (frame_rgb, detections) with the same format
# Example (pseudo):
#   from ultralytics import YOLO
#   @st.cache_resource
#   def load_model(path): return YOLO(path)
#   def run_inference(model, frame):
#       results = model.predict(source=frame, imgsz=640, conf=0.35, verbose=False)
#       ... convert results to detections list above ...
# Keep the same detections format and the pages won't require changes.
# -----------------------------
