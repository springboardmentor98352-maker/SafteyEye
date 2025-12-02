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
from core.logger import log_violation, CSV_PATH
from core.emailer import send_email_alert   # <-- NEW

# ---------------------
# Config / defaults
# ---------------------
LOG_COOLDOWN = 5.0      # seconds cooldown per person to avoid repeated log spam
EMAIL_COOLDOWN = 60.0   # seconds between email alerts (global)
DEFAULT_WEIGHTS = "models/best.pt"
DEFAULT_CONF = 0.35
DEFAULT_RUN_RATE = 8    # fps

st.set_page_config(layout="wide", page_title="SafetyEye")
st.title("SafetyEye — Workplace Occupancy & PPE Monitor")

# ---------------------
# Left / Right panels
# ---------------------
col_left, col_right = st.columns([2, 1])

# -------- LEFT: video source & preview --------
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

# -------- RIGHT: controls, logs, email --------
with col_right:
    st.header("Controls & Logs")
    conf_slider = st.slider("Confidence threshold", 0.1, 0.9, DEFAULT_CONF, 0.05)
    run_rate = st.number_input(
        "Max FPS (approx)", min_value=1, max_value=30, value=DEFAULT_RUN_RATE
    )

    st.write("Recent violations:")
    if os.path.exists(CSV_PATH):
        try:
            df_logs = pd.read_csv(CSV_PATH)
            st.dataframe(df_logs.tail(8))
        except Exception:
            st.write("No logs yet or CSV malformed.")
    else:
        st.write("No logs yet.")

    # -------------------------
    # Email Alerts (moved here)
    # -------------------------
    st.markdown("---")
    st.header("Email Alerts (optional)")

    enable_email = st.checkbox("Enable email alerts")
    smtp_host = st.text_input("SMTP host", "smtp.gmail.com")
    smtp_port = st.number_input("SMTP port", 1, 65535, 465)
    use_ssl = st.checkbox("Use SSL (recommended for Gmail)", value=True)

    smtp_user = st.text_input("Sender email (SMTP user)")
    smtp_password = st.text_input(
        "Email password / app password", type="password"
    )
    recipient = st.text_input("Recipient email")


# ---------------------
# Detector resource
# ---------------------
@st.cache_resource
def get_detector(weights=DEFAULT_WEIGHTS, conf=DEFAULT_CONF):
    return Detector(weights_path=weights, conf=conf)


detector = get_detector(conf=conf_slider)

# ---------------------
# Session state flags
# ---------------------
if "running" not in st.session_state:
    st.session_state.running = False
if "last_log_time" not in st.session_state:
    st.session_state.last_log_time = {}  # person_idx -> timestamp
if "last_frame_time" not in st.session_state:
    st.session_state.last_frame_time = 0.0
if "temp_video" not in st.session_state:
    st.session_state.temp_video = None
if "last_email_time" not in st.session_state:
    st.session_state.last_email_time = 0.0

# Start / stop controls
if start_btn:
    st.session_state.running = True
if stop_btn:
    st.session_state.running = False

# ---------------------
# Video capture initialization
# ---------------------
cap = None
temp_file = None

if st.session_state.running:
    if source_select == "Webcam":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error(
                "Unable to open webcam. Make sure no other app is using it and permissions are granted."
            )
            st.session_state.running = False
    else:
        if uploaded_file is None:
            st.warning("Please upload a video file to start.")
            st.session_state.running = False
        else:
            temp_file = "temp_upload_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.temp_video = temp_file
            cap = cv2.VideoCapture(temp_file)
            if not cap.isOpened():
                st.error("Unable to open uploaded video file.")
                st.session_state.running = False

# ---------------------
# Main detection loop
# ---------------------
try:
    violations = []
    violation_boxes = []

    min_interval = 1.0 / float(run_rate)

    while st.session_state.running and cap and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # video finished or camera disconnected
            break

        # throttle FPS so Streamlit is responsive
        now = time.time()
        if now - st.session_state.last_frame_time < min_interval:
            time.sleep(0.005)
            continue
        st.session_state.last_frame_time = now

        # Run prediction
        detections = detector.predict(frame)

        # Map PPE detections to persons and evaluate violations
        mapping = match_ppe_to_person(detections, iou_thresh=0.12)
        violations, violation_boxes = evaluate_violations(
            mapping, conf_threshold=conf_slider
        )

        # Log violations using a cooldown per person index
        for v in violations:
            pid = v.get("person_idx", None)
            person_box = v.get("person_box", (0, 0, 0, 0))
            miss_helmet = v.get("missing_helmet", False)
            miss_vest = v.get("missing_vest", False)

            if pid is None:
                # log once without cooldown when id missing
                log_violation(-1, miss_helmet, miss_vest, "", person_box, frame)
                continue

            last = st.session_state.last_log_time.get(pid, 0)
            if time.time() - last >= LOG_COOLDOWN:
                conf_summary = ""  # optional future extension
                log_violation(pid, miss_helmet, miss_vest, conf_summary, person_box, frame)
                st.session_state.last_log_time[pid] = time.time()

        # ------------- Email alert block -------------
        if (
            enable_email
            and len(violations) > 0
            and smtp_host
            and smtp_user
            and smtp_password
            and recipient
        ):
            now_email = time.time()
            if now_email - st.session_state.last_email_time >= EMAIL_COOLDOWN:
                # Build a simple summary email
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                subject = f"[SafetyEye] PPE Violations Detected at {ts}"
                lines = [f"Total violations in this interval: {len(violations)}", ""]
                for v in violations:
                    idx = v.get("person_idx", -1)
                    mh = v.get("missing_helmet", False)
                    mv = v.get("missing_vest", False)
                    lines.append(
                        f"Person {idx}: "
                        f"{'Missing helmet' if mh else 'Helmet OK'}, "
                        f"{'Missing vest' if mv else 'Vest OK'}"
                    )
                body = "\n".join(lines)

                try:
                    ok = send_email_alert(
                        smtp_host=smtp_host,
                        smtp_port=int(smtp_port),
                        smtp_user=smtp_user,
                        smtp_password=smtp_password,
                        subject=subject,
                        body=body,
                        to_addrs=[recipient],
                        use_ssl=use_ssl,
                    )
                    if ok:
                        st.session_state.last_email_time = now_email
                    else:
                        st.warning("Failed to send email alert (see console log).")
                except Exception as e:
                    st.warning(f"Email sending failed: {e}")
        # -------------------------------------------

        # Draw boxes on the frame
        frame_out = draw_boxes(frame.copy(), detections, violation_boxes)

        # Convert BGR -> RGB for display
        frame_rgb = cv2.cvtColor(frame_out, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        frame_display.image(img, use_column_width=True)

        # Show small status
        if len(violations) > 0:
            st.warning(f"Violations detected: {len(violations)}")
        else:
            st.success("No violations detected")

    # finished loop: release capture
    if cap:
        cap.release()

except Exception as e:
    if cap:
        cap.release()
    st.error(f"Detection loop error: {e}")
    raise

finally:
    # cleanup temporary uploaded video file if any
    if st.session_state.get("temp_video"):
        try:
            os.remove(st.session_state["temp_video"])
        except Exception:
            pass
        st.session_state["temp_video"] = None
