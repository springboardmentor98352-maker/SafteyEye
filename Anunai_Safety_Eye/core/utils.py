# core/utils.py
import cv2
import numpy as np
from typing import Tuple, Dict

def draw_boxes(frame: np.ndarray, detections: list, violation_boxes: list=None) -> np.ndarray:
    """
    Draws boxes on frame. violation_boxes is list of boxes to draw in red.
    Each detection is a dict with 'box', 'label', 'conf'.
    Returns modified frame (BGR).
    """
    if violation_boxes is None:
        violation_boxes = []

    for d in detections:
        x1, y1, x2, y2 = d['box']
        label = f"{d['label']} {d['conf']:.2f}"
        color = (0, 200, 0)  # green normal
        # mark violation if this exact box in violation list (by bbox equality)
        if any(b == d['box'] for b in violation_boxes):
            color = (0, 0, 255)  # red
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        # text background
        ((tw, th), _) = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw, y1), color, -1)
        cv2.putText(frame, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1, cv2.LINE_AA)
    return frame

def iou(boxA: Tuple[int,int,int,int], boxB: Tuple[int,int,int,int]) -> float:
    xA = max(boxA[0], boxB[0]); yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2]); yB = min(boxA[3], boxB[3])
    interW = max(0, xB - xA); interH = max(0, yB - yA)
    interArea = interW * interH
    boxAArea = max(1, (boxA[2] - boxA[0])) * max(1, (boxA[3] - boxA[1]))
    boxBArea = max(1, (boxB[2] - boxB[0])) * max(1, (boxB[3] - boxB[1]))
    union = boxAArea + boxBArea - interArea
    return interArea / union if union > 0 else 0.0

def center(box):
    x1,y1,x2,y2 = box
    return ((x1+x2)/2.0, (y1+y2)/2.0)
