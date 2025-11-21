"""
core/rules.py

Simple rule engine that consumes detections and returns violation structures.
This file is intentionally simple: it allows replacement with a more advanced
tracker-based engine later (TODO added).
"""

from typing import List, Dict, Tuple

def detect_violations(detections: List[Dict], required_ppe: Tuple[str, ...] = ("helmet", "vest")):
    """
    Given detections (list of dicts produced by inference), return list of violation objects.

    Each returned violation is:
    {
      "person_id": int or None,
      "missing": ["helmet", ...],
      "person_bbox": (x1,y1,x2,y2)
    }
    """
    violations = []
    for d in detections:
        missing = d.get("missing", [])
        if missing:
            violations.append({
                "person_id": d.get("person_id"),
                "missing": missing,
                "person_bbox": d.get("bbox")
            })
    return violations

# TODO: ADD_TRACKER
# When YOLOv8 is integrated, add a tracker wrapper (ByteTrack/DeepSort) to provide persistent
# person_id across frames. Keep detect_violations signature unchanged so pages don't change.
