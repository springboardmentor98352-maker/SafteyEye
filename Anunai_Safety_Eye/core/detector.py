# core/detector.py
from ultralytics import YOLO
import numpy as np
import cv2
from typing import List, Dict, Tuple, Any


class Detector:
    """
    Simple wrapper around ultralytics YOLO model for frame-by-frame inference.
    Returns normalized, consistent detection dicts.
    """
    def __init__(self, weights_path: str = "models/best.pt", device: str = None, conf: float = 0.35, imgsz: int = 640):
        # Uses Ultralytics YOLO; if device left None it auto-selects cpu/gpu.
        # Optionally you can pass device="cuda:0" to use GPU.
        self.model = YOLO(weights_path)
        self.conf = conf
        self.imgsz = imgsz
        # extract names if available
        try:
            # ultralytics Model.model.names is usually a dict map idx->name
            self.names = self.model.model.names
        except Exception:
            # fallback minimal mapping (you should have names in model)
            self.names = {i: str(i) for i in range(100)}

    def _ensure_labels(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Defensive normalization so that every detection dict contains a 'label' string.
        - If 'label' already exists and is truthy, keep it (but normalize to lowercase string).
        - Otherwise, attempt to derive label from numeric class index keys like 'cls' or 'class'.
        Returns a new list (or modifies in-place) of detection dicts with 'label' present.
        """
        normalized = []
        for d in detections:
            # if label exists and is not None/empty, normalize it to string (lowercase)
            if 'label' in d and d['label'] is not None and str(d['label']).strip() != "":
                try:
                    d['label'] = str(d['label']).lower()
                except Exception:
                    d['label'] = str(d['label'])
                normalized.append(d)
                continue

            # try common numeric keys that may hold class index
            cls_idx = None
            for key in ('cls', 'class', 'class_id', 'category'):
                if key in d and d[key] is not None:
                    try:
                        cls_idx = int(d[key])
                        break
                    except Exception:
                        # not an int-like value; continue searching
                        continue

            # map index -> name using self.names if available
            if cls_idx is not None and hasattr(self, 'names'):
                try:
                    name = self.names.get(cls_idx, str(cls_idx))
                except Exception:
                    name = str(cls_idx)
            else:
                # fallback: try any text-like fields that might contain label
                name = d.get('name') or d.get('class_name') or d.get('label') or d.get('label_text') or ""
            # ensure label key exists as lowercase string
            try:
                d['label'] = str(name).lower()
            except Exception:
                d['label'] = str(name)
            normalized.append(d)
        return normalized

    def predict(self, frame: np.ndarray) -> List[Dict]:
        """
        frame: BGR OpenCV image (H,W,3)
        returns list of detections:
          [{'box':(x1,y1,x2,y2), 'conf':float, 'cls':int, 'label':str}]
        Coordinates are in pixel units (int).
        """
        # Ultralytics accepts BGR images directly.
        results = self.model(frame, imgsz=self.imgsz, conf=self.conf, verbose=False)
        # results may be a list-like or single Results
        res = results[0] if isinstance(results, (list, tuple)) else results
        detections: List[Dict] = []

        # res.boxes is a Boxes object; handle gracefully
        try:
            boxes_obj = getattr(res, "boxes", None)
        except Exception:
            boxes_obj = None

        if boxes_obj is not None and len(boxes_obj) > 0:
            for i, box in enumerate(boxes_obj):
                # xyxy may be a tensor-like; convert safely
                try:
                    # many ultralytics versions use box.xyxy as a tensor with shape (1,4)
                    xyxy_arr = box.xyxy[0].cpu().numpy() if hasattr(box.xyxy[0], "cpu") else box.xyxy[0].numpy() if hasattr(box.xyxy[0], "numpy") else np.array(box.xyxy[0])
                    conf_val = float(box.conf[0].cpu().numpy()) if hasattr(box.conf[0], "cpu") else float(box.conf[0])
                    cls_id = int(box.cls[0].cpu().numpy()) if hasattr(box.cls[0], "cpu") else int(box.cls[0])
                except Exception:
                    # final fallback: try attributes directly
                    try:
                        xyxy_arr = np.array(box.xyxy).reshape(-1)[:4]
                    except Exception:
                        # as last resort, skip this box
                        continue
                    try:
                        conf_val = float(getattr(box, "conf", 0.0))
                    except Exception:
                        conf_val = 0.0
                    try:
                        cls_id = int(getattr(box, "cls", -1))
                    except Exception:
                        cls_id = -1

                # convert coords to ints
                try:
                    x1, y1, x2, y2 = map(int, xyxy_arr[:4])
                except Exception:
                    # skip malformed box
                    continue

                # map class index -> label (string)
                try:
                    label = self.names.get(cls_id, str(cls_id))
                except Exception:
                    label = str(cls_id)

                # normalize label to string but don't lowercase here (we'll ensure later)
                detections.append({
                    'box': (x1, y1, x2, y2),
                    'conf': float(conf_val),
                    'cls': int(cls_id),
                    'label': str(label)
                })

        # ensure every detection has a 'label' string (lowercased)
        detections = self._ensure_labels(detections)
        return detections
