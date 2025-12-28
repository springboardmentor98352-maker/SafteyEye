import cv2
import os
import time
from collections import deque
from ultralytics import YOLO
from . import utils as pdf_utils
from app.pages.settings import load_settings

MODEL_PATH = "model/best.pt"
model = YOLO(MODEL_PATH)

FRAME_WINDOW = 5
person_mask_buffer = {}
person_helmet_buffer = {}
person_vest_buffer = {}
violation_cooldown = 5
last_violation_time = {}
PERSON_ID_COUNTER = 0

def detect_violations(frame):
    global PERSON_ID_COUNTER
    settings = load_settings()
    results = model(frame, conf=settings.get("confidence_threshold",0.35), verbose=False)[0]
    violations_frame = []
    persons_in_frame = []

    for box in results.boxes:
        label = model.names[int(box.cls[0])].lower()
        conf = float(box.conf[0])

        if label == "person" and conf >= 0.40:
            person_id = PERSON_ID_COUNTER
            PERSON_ID_COUNTER += 1
            persons_in_frame.append(person_id)

            if person_id not in person_mask_buffer:
                person_mask_buffer[person_id] = deque(maxlen=FRAME_WINDOW)
                person_helmet_buffer[person_id] = deque(maxlen=FRAME_WINDOW)
                person_vest_buffer[person_id] = deque(maxlen=FRAME_WINDOW)

            mask_seen = helmet_seen = vest_seen = False
            for pbox in results.boxes:
                plabel = model.names[int(pbox.cls[0])].lower()
                pconf = float(pbox.conf[0])
                if plabel == "mask" and pconf >= 0.20:
                    mask_seen = True
                elif plabel == "helmet" and pconf >= 0.25:
                    helmet_seen = True
                elif plabel in ["vest","safety vest"] and pconf >= 0.25:
                    vest_seen = True

            person_mask_buffer[person_id].append(mask_seen)
            person_helmet_buffer[person_id].append(helmet_seen)
            person_vest_buffer[person_id].append(vest_seen)

            person_violations = []
            if sum(person_mask_buffer[person_id]) < FRAME_WINDOW // 2:
                person_violations.append("NO-MASK")
            if sum(person_helmet_buffer[person_id]) < FRAME_WINDOW // 2:
                person_violations.append("NO-HARDHAT")
            if sum(person_vest_buffer[person_id]) < FRAME_WINDOW // 2:
                person_violations.append("NO-SAFETY VEST")

            now = time.time()
            last_time = last_violation_time.get(person_id, 0)
            if person_violations and (now - last_time) > violation_cooldown:
                violations_frame.extend(person_violations)
                last_violation_time[person_id] = now

    return violations_frame, results

def count_people(results):
    return sum(1 for box in results.boxes if model.names[int(box.cls[0])].lower() == "person")

def save_violation(violations, frame, confidence=1.0):
    os.makedirs("database/images", exist_ok=True)
    vid = f"V_{int(time.time())}"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    img_path = os.path.join("database/images", f"{vid}.jpg")

    annotated = frame.copy()
    y = 40
    for v in violations:
        cv2.putText(annotated, v, (10,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        y += 45
    cv2.imwrite(img_path, annotated)

    if load_settings().get("generate_pdf", True):
        pdf_utils.generate_pdf(
            vid=vid,
            label=",".join(violations),
            image_path=img_path,
            timestamp=timestamp,
            confidence=confidence
        )
    return img_path, vid, timestamp
