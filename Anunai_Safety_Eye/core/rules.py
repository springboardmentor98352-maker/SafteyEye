# core/rules.py
from typing import List, Dict, Tuple
from core.utils import iou, center

# ---------- helpers ----------

def safe_label(det: Dict) -> str:
    """
    Safely get a lowercase label string from a detection dict.
    Works even if 'label' key is missing.
    """
    if not isinstance(det, dict):
        return ""

    # 1) Existing label
    if "label" in det and det["label"] is not None:
        try:
            return str(det["label"]).lower()
        except Exception:
            return str(det["label"])

    # 2) Numeric class id fields
    for key in ("cls", "class", "class_id", "category"):
        if key in det and det[key] is not None:
            try:
                return str(int(det[key]))  # e.g. "0", "1"
            except Exception:
                return str(det[key]).lower()

    # 3) Other text-like fields
    for key in ("name", "class_name", "label_text"):
        if key in det and det[key]:
            try:
                return str(det[key]).lower()
            except Exception:
                return str(det[key])

    return ""


def has_valid_box(det: Dict) -> bool:
    """
    Return True only if det has a valid 'box' with 4 numbers.
    """
    if not isinstance(det, dict):
        return False
    if "box" not in det:
        return False
    box = det.get("box")
    if not isinstance(box, (list, tuple)):
        return False
    if len(box) != 4:
        return False
    return True


# ---------- main mapping: detections -> persons + ppe ----------

def match_ppe_to_person(
    detections: List[Dict],
    iou_thresh: float = 0.15
) -> Dict[int, Dict]:
    """
    Assign PPE detections (helmet/vest etc.) to person detections.

    Returns a dict:
      {
        person_idx: {
           "person": <person_det>,
           "ppe": [<ppe_det_1>, <ppe_det_2>, ...]
        },
        ...
      }
    This shape is what `evaluate_violations` expects.
    """

    # 0) Clean detections: drop anything without a valid 'box'
    cleaned: List[Dict] = [d for d in detections if has_valid_box(d)]

    # 1) separate persons from other detections
    persons: List[Dict] = []
    others: List[Dict] = []

    for d in cleaned:
        lab = safe_label(d)
        # treat "person" or "people" or "0" (if numeric class 0) as person
        if lab in ("person", "people", "0"):
            persons.append(d)
        else:
            others.append(d)

    mapping: Dict[int, Dict] = {}
    for idx, p in enumerate(persons):
        mapping[idx] = {"person": p, "ppe": []}

    # 2) assign each non-person (ppe) to closest person by IoU first
    for ppe_det in others:
        ppe_box = ppe_det["box"]  # safe because cleaned ensured 'box' exists
        assigned = False
        best_iou = 0.0
        best_idx = None

        for idx, info in mapping.items():
            p_box = info["person"]["box"]
            ov = iou(p_box, ppe_box)
            if ov > best_iou and ov >= iou_thresh:
                best_iou = ov
                best_idx = idx

        if best_idx is not None:
            mapping[best_idx]["ppe"].append(ppe_det)
            assigned = True

        # 3) If not assigned by IoU, try center-in-person-box as backup
        if not assigned:
            cx, cy = center(ppe_box)
            for idx, info in mapping.items():
                x1, y1, x2, y2 = info["person"]["box"]
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    mapping[idx]["ppe"].append(ppe_det)
                    assigned = True
                    break
        # if still not assigned, we ignore this PPE

    return mapping


# ---------- violation evaluation ----------

def evaluate_violations(
    mapping: Dict[int, Dict],
    conf_threshold: float = 0.35
) -> Tuple[List[Dict], List[Tuple[int, int, int, int]]]:
    """
    Given mapping from person_idx -> {"person": person_det, "ppe": [ppe_dets]},
    compute PPE violations.

    Returns:
      violations: list of dicts like:
        {
          "person_idx": idx,
          "person_box": (x1,y1,x2,y2),
          "missing_helmet": bool,
          "missing_vest": bool,
          "details": { ... }
        }

      violation_boxes: list of person boxes to highlight in red.
    """
    violations: List[Dict] = []
    violation_boxes: List[Tuple[int, int, int, int]] = []

    # If mapping accidentally comes as a list, convert it (failsafe)
    if isinstance(mapping, list):
        tmp = {}
        for item in mapping:
            try:
                idx = int(item.get("person_idx", 0))
            except Exception:
                idx = 0
            tmp[idx] = {
                "person": {"box": item.get("person_box", (0, 0, 0, 0))},
                "ppe": []
            }
        mapping = tmp

    for idx, info in mapping.items():
        person = info.get("person", {})
        ppe_list = info.get("ppe", [])

        person_box = person.get("box", (0, 0, 0, 0))

        # defaults
        has_helmet = False
        has_no_helmet = False
        has_vest = False
        has_no_vest = False

        for p in ppe_list:
            lab = safe_label(p)
            c = float(p.get("conf", 0.0))
            if lab == "helmet" and c >= conf_threshold:
                has_helmet = True
            elif lab == "no_helmet" and c >= conf_threshold:
                has_no_helmet = True
            elif lab == "vest" and c >= conf_threshold:
                has_vest = True
            elif lab == "no_vest" and c >= conf_threshold:
                has_no_vest = True

        missing_helmet = (not has_helmet) or has_no_helmet
        missing_vest = (not has_vest) or has_no_vest

        if missing_helmet or missing_vest:
            violation_boxes.append(person_box)
            violations.append({
                "person_idx": idx,
                "person_box": person_box,
                "missing_helmet": missing_helmet,
                "missing_vest": missing_vest,
                "details": {
                    "has_helmet": has_helmet,
                    "has_no_helmet": has_no_helmet,
                    "has_vest": has_vest,
                    "has_no_vest": has_no_vest,
                }
            })

    return violations, violation_boxes


# ---------- compatibility wrapper for live_monitor.py ----------

def detect_violations(
    detections: List[Dict],
    iou_thresh: float = 0.15,
    conf_threshold: float = 0.35
) -> List[Dict]:
    """
    Backwards-compatible function for pages/live_monitor.py.

    It takes raw detections, runs mapping + evaluation,
    and returns ONLY the list of violations.
    """
    mapping = match_ppe_to_person(detections, iou_thresh=iou_thresh)
    violations, _ = evaluate_violations(mapping, conf_threshold=conf_threshold)
    return violations
