# app.py
import streamlit as st
import cv2
import os
import time
from PIL import Image
import pandas as pd

from core.detector import Detector
from core.rules import match_ppe_to_person, evaluate_violations
from core.utils import draw_boxes
from core import storage
from core.emailer import send_email_alert

# ---------------------
# Config / defaults
# ---------------------
LOG_COOLDOWN = 5.0       # seconds cooldown per person
EMAIL_COOLDOWN = 60.0    # seconds between email alerts
DEFAULT_WEIGHTS = "models/best.pt"
DEFAULT_CONF = 0.35
DEFAULT_RUN_RATE = 8     # fps

st.set_page_config(layout="wide", page_title="SafetyEye")
st.title("SafetyEye — Workplace Occupancy & PPE Monitor")

# ---------------------
# Layout
# ---------------------
col_left, col_right = st.columns([2, 1])

# -------- LEFT: video source --------
with col_left:
    st.header("Live Camera")
    frame_display = st.empty()
    start_btn = st.button("Start")
    stop_btn = st.button("Stop")
    source_select = st.selectbox("Input source", ["Webcam", "Upload video"])
    uploaded_file = (
        st.file_uploader("Upload video (mp4)", type=["mp4", "mov", "avi"])
        if source_select == "Upload video"
        else None
    )

# -------- RIGHT: controls & logs --------
with col_right:
    st.header("Controls & Logs")
    conf_slider = st.slider("Confidence threshold", 0.1, 0.9, DEFAULT_CONF, 0.05)
    run_rate = st.number_input("Max FPS (approx)", 1, 30, DEFAULT_RUN_RATE)

    st.write("Recent logs:")
    rows = storage.read_logs(limit=20)
    if rows:
        st.dataframe(pd.DataFrame(rows))
    else:
        st.write("No logs yet.")

    # -------- Email alerts --------
    st.markdown("---")
    st.header("Email Alerts (optional)")
    enable_email = st.checkbox("Enable email alerts")
    smtp_host = st.text_input("SMTP host", "smtp.gmail.com")
    smtp_port = st.number_input("SMTP port", 1, 65535, 465)
    use_ssl = st.checkbox("Use SSL", value=True)
    smtp_user = st.text_input("Sender email")
    smtp_password = st.text_input("Email password / app password", type="password")
    recipient = st.text_input("Recipient email")

# ---------------------
# Detector (cached)
# ---------------------
@st.cache_resource
def get_detector(weights, conf):
    return Detector(weights_path=weights, conf=conf)

detector = get_detector(DEFAULT_WEIGHTS, conf_slider)

# ---------------------
# Session state
# ---------------------
if "running" not in st.session_state:
    st.session_state.running = False
if "last_log_time" not in st.session_state:
    st.session_state.last_log_time = {}
if "last_frame_time" not in st.session_state:
    st.session_state.last_frame_time = 0.0
if "last_email_time" not in st.session_state:
    st.session_state.last_email_time = 0.0
if "temp_video" not in st.session_state:
    st.session_state.temp_video = None

# Start / stop
if start_btn:
    st.session_state.running = True
if stop_btn:
    st.session_state.running = False

# ---------------------
# Video capture
# ---------------------
cap = None

if st.session_state.running:
    if source_select == "Webcam":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Unable to open webcam.")
            st.session_state.running = False
    else:
        if uploaded_file is None:
            st.warning("Upload a video to start.")
            st.session_state.running = False
        else:
            temp_path = "temp_video.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.temp_video = temp_path
            cap = cv2.VideoCapture(temp_path)

# ---------------------
# Main loop
# ---------------------
try:
    min_interval = 1.0 / float(run_rate)

    while st.session_state.running and cap and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        if now - st.session_state.last_frame_time < min_interval:
            time.sleep(0.005)
            continue
        st.session_state.last_frame_time = now

        # Detection
        detections = detector.predict(frame)

        mapping = match_ppe_to_person(detections, iou_thresh=0.12)
        violations, violation_boxes = evaluate_violations(
            mapping, conf_threshold=conf_slider
        )

        # -------- Frame summary log --------
        storage.append_log({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "frame_id": "",
            "people_count": len(mapping),
            "violations_count": len(violations),
            "person_id": "",
            "missing": ""
        })

        # -------- Violation logs --------
        for v in violations:
            pid = v.get("person_idx", -1)
            miss_helmet = v.get("missing_helmet", False)
            miss_vest = v.get("missing_vest", False)

            last = st.session_state.last_log_time.get(pid, 0)
            if time.time() - last < LOG_COOLDOWN:
                continue

            missing = []
            if miss_helmet:
                missing.append("helmet")
            if miss_vest:
                missing.append("vest")

            storage.append_log({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "frame_id": "",
                "people_count": len(mapping),
                "violations_count": 1,
                "person_id": f"person_{pid}",
                "missing": ",".join(missing)
            })

            st.session_state.last_log_time[pid] = time.time()

        # -------- Email alerts --------
        if (
            enable_email and violations and smtp_host and smtp_user
            and smtp_password and recipient
        ):
            now_email = time.time()
            if now_email - st.session_state.last_email_time >= EMAIL_COOLDOWN:
                subject = "[SafetyEye] PPE Violations Detected"
                body = f"Total violations: {len(violations)}"
                ok = send_email_alert(
                    smtp_host, int(smtp_port), smtp_user,
                    smtp_password, subject, body,
                    [recipient], use_ssl
                )
                if ok:
                    st.session_state.last_email_time = now_email

        # Draw boxes
        frame_out = draw_boxes(frame.copy(), detections, violation_boxes)
        frame_rgb = cv2.cvtColor(frame_out, cv2.COLOR_BGR2RGB)
        frame_display.image(Image.fromarray(frame_rgb), use_column_width=True)

        if violations:
            st.warning(f"Violations detected: {len(violations)}")
        else:
            st.success("No violations detected")

    if cap:
        cap.release()

finally:
    if st.session_state.get("temp_video"):
        try:
            os.remove(st.session_state["temp_video"])
        except Exception:
            pass
        st.session_state["temp_video"] = None

