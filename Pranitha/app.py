# ======================================================
# SafetyEye Backend Application
# ======================================================

import cv2
import time
import base64
import uuid
import threading
from collections import defaultdict

from flask import Flask
from flask_socketio import SocketIO
from ultralytics import YOLO

# ======================================================
# CONFIG
# ======================================================

YOLO_CONF = 0.4
INFERENCE_INTERVAL = 0.2

PPE_CONFIRM_SEC = 3.0
PPE_ESCALATE_SEC = 8.0
RESOLVE_GRACE_SEC = 2.0
CONFIDENCE_WINDOW_SEC = 10.0

TRACK_IOU_THRESHOLD = 0.4
TRACK_TTL_SEC = 2.5        
COMPLIANCE_WINDOW_SEC = 60.0

VIOLATION_COOLDOWN_SEC = 15.0

# ======================================================
# STATES & RISK WEIGHTS
# ======================================================

CONFIRMED = "CONFIRMED"
ESCALATED = "ESCALATED"
RESOLVED  = "RESOLVED"

RISK_WEIGHTS = {
    CONFIRMED: 15,
    ESCALATED: 40
}


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

model = YOLO("detectors/best.pt")
model_lock = threading.Lock()

# ======================================================
# CAMERAS
# ======================================================

CAMERAS = {
    "cam1": "videos/cam1.mp4",
    "cam2": "videos/cam2.mp4",
    "cam3": "videos/cam3.mp4",
    "cam4": "videos/cam4.mp4",
}

# ======================================================
# GLOBAL STATE
# ======================================================

raw_frames = {}
frame_locks = defaultdict(threading.Lock)

tracks = defaultdict(dict)
next_tid = defaultdict(int)

person_state = {}
violation_events = []
compliance_time = defaultdict(list)
last_violation_time = {}

# ======================================================
# UTILS
# ======================================================

def iou(a, b):
    xA, yA = max(a[0], b[0]), max(a[1], b[1])
    xB, yB = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (a[2]-a[0])*(a[3]-a[1])
    areaB = (b[2]-b[0])*(b[3]-b[1])
    return inter / (areaA + areaB - inter + 1e-6)

def point_inside(box, px, py):
    return box[0] <= px <= box[2] and box[1] <= py <= box[3]

def risk_level(score):
    if score >= 70: return "HIGH"
    if score >= 30: return "MEDIUM"
    return "LOW"

# ======================================================
# CAMERA READER
# ======================================================

def camera_reader(cam_id, path):
    cap = cv2.VideoCapture(path)
    while True:
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        with frame_locks[cam_id]:
            raw_frames[cam_id] = frame
        time.sleep(0.03)

# ======================================================
# VIOLATION MANAGEMENT
# ======================================================

def create_violation(cam, tid, vtype, start):
    now = time.time()
    key = (cam, tid, vtype)

    if key in last_violation_time and now - last_violation_time[key] < VIOLATION_COOLDOWN_SEC:
        return

    last_violation_time[key] = now

    violation_events.append({
        "event_id": str(uuid.uuid4()),
        "camera_id": cam,
        "person_id": tid,
        "type": vtype,
        "state": CONFIRMED,
        "start_time": start,
        "last_seen": start,
        "end_time": None,
        "resolved": False,
    })

def resolve_violation(cam, tid, vtype):
    now = time.time()
    for v in violation_events:
        if not v["resolved"] and v["camera_id"] == cam and v["person_id"] == tid and v["type"] == vtype:
            v["resolved"] = True
            v["state"] = RESOLVED
            v["end_time"] = now

def serialize_violation(v):
    now = time.time()
    duration = (v["end_time"] or now) - v["start_time"]
    confidence = min(1.0, duration / CONFIDENCE_WINDOW_SEC)
    return {
        "type": v["type"],
        "state": v["state"],
        "duration": round(duration, 1),
        "confidence": int(confidence * 100)
    }

# ======================================================
# AI WORKER
# ======================================================

def ai_worker(cam_id):
    while True:
        time.sleep(INFERENCE_INTERVAL)

        with frame_locks[cam_id]:
            frame = raw_frames.get(cam_id)
        if frame is None:
            continue

        with model_lock:
            result = model(frame, conf=YOLO_CONF, verbose=False)[0]

        now = time.time()
        canvas = frame.copy()

        persons, miss_hat, miss_mask, miss_vest = [], [], [], []

        for box in result.boxes:
            label = model.names[int(box.cls[0])].lower().strip()
            bbox = tuple(map(int, box.xyxy[0]))

            if label == "person":
                persons.append(bbox)

            elif "hardhat" in label or "helmet" in label:
                miss_hat.append(bbox)
            elif "mask" in label and "no" in label:
                miss_mask.append(bbox)

            elif "vest" in label and "no" in label:
                miss_vest.append(bbox)

        # ---- TRACKING ----
        current_tracks = {}
        for bbox in persons:
            best_iou, best_tid = 0, None
            for tid, trk in tracks[cam_id].items():
                ov = iou(bbox, trk["bbox"])
                if ov > best_iou:
                    best_iou, best_tid = ov, tid

            if best_iou > TRACK_IOU_THRESHOLD:
                tracks[cam_id][best_tid]["bbox"] = bbox
                tracks[cam_id][best_tid]["last_seen"] = now
                current_tracks[best_tid] = bbox
            else:
                tid = next_tid[cam_id]
                next_tid[cam_id] += 1
                tracks[cam_id][tid] = {"bbox": bbox, "last_seen": now}
                current_tracks[tid] = bbox

        tracks[cam_id] = {
            tid: trk for tid, trk in tracks[cam_id].items()
            if now - trk["last_seen"] <= TRACK_TTL_SEC
        }

        persons_payload = []
        high_risk_present = False

        # ---- PPE  ----
        for tid, bbox in current_tracks.items():
            key = (cam_id, tid)
            person_state.setdefault(key, {
                "hat_missing": None, "hat_clear": None,
                "mask_missing": None, "mask_clear": None,
                "vest_missing": None, "vest_clear": None,
            })

            state = person_state[key]
            active_violations = []

            def process(flag, miss, label):
                start = state[flag]
                clear = state[f"{flag.replace('_missing','')}_clear"]

                if miss:
                    state[flag] = start or now
                    state[f"{flag.replace('_missing','')}_clear"] = None
                    dur = now - state[flag]

                    if dur >= PPE_CONFIRM_SEC:
                        existing = [v for v in violation_events if not v["resolved"] and v["camera_id"] == cam_id and v["person_id"] == tid and v["type"] == label]
                        if not existing:
                            create_violation(cam_id, tid, label, state[flag])
                        else:
                            existing[0]["last_seen"] = now
                            if dur >= PPE_ESCALATE_SEC:
                                existing[0]["state"] = ESCALATED
                else:
                    state[flag] = None
                    state[f"{flag.replace('_missing','')}_clear"] = clear or now
                    if now - state[f"{flag.replace('_missing','')}_clear"] >= RESOLVE_GRACE_SEC:
                        resolve_violation(cam_id, tid, label)

            #  HARDHAT 
            process(
                "hat_missing",
                any(point_inside(bbox, (b[0]+b[2])//2, (b[1]+b[3])//2) for b in miss_hat),
                "NO HARDHAT"
            )

            process("mask_missing", any(iou(bbox,b) > 0.01 for b in miss_mask), "NO MASK")
            process("vest_missing", any(iou(bbox,b) > 0.05 for b in miss_vest), "NO VEST")

            risk = 0
            for v in violation_events:
                if not v["resolved"] and v["camera_id"] == cam_id and v["person_id"] == tid:
                    risk += RISK_WEIGHTS[v["state"]]
                    active_violations.append(serialize_violation(v))

            risk = min(100, risk)
            level = risk_level(risk)
            if risk >= 30:
                high_risk_present = True

            persons_payload.append({
                "personId": f"P-{tid:02d}",
                "risk": risk,
                "riskLevel": level,
                "violations": active_violations
            })

            color = (0,0,255) if level=="HIGH" else (0,165,255) if level=="MEDIUM" else (0,255,0)
            cv2.rectangle(canvas, bbox[:2], bbox[2:], color, 2)
            cv2.putText(canvas, f"P-{tid:02d} {level}", (bbox[0], bbox[1]-6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # ---- COMPLIANCE ----
        cam_safe = not high_risk_present
        compliance_time[cam_id].append((now, cam_safe))
        compliance_time[cam_id] = [(t,ok) for t,ok in compliance_time[cam_id] if now-t<=COMPLIANCE_WINDOW_SEC]

        safe = sum(1 for _,ok in compliance_time[cam_id] if ok)
        total = len(compliance_time[cam_id])
        compliance = int((safe/total)*100) if total else 100

        active_cam_violations = sum(
            len(p["violations"]) for p in persons_payload
        )

        ok, jpg = cv2.imencode(".jpg", canvas)
        if not ok:
            continue

        socketio.emit("camera_event", {
            "camId": cam_id,
            "frame": base64.b64encode(jpg).decode(),
            "persons": persons_payload,
            "occupancy": len(current_tracks),
            "ppeCompliance": compliance,
            "activeViolations": active_cam_violations,
            "ts": int(now * 1000)
        })

# ======================================================
# ENTRY
# ======================================================

if __name__ == "__main__":
    for cam, path in CAMERAS.items():
        threading.Thread(target=camera_reader, args=(cam,path), daemon=True).start()
        threading.Thread(target=ai_worker, args=(cam,), daemon=True).start()

    socketio.run(app, host="0.0.0.0", port=5001)
