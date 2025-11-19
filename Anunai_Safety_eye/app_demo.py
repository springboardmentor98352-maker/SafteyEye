# python -m streamlit run app_demo.py

# # SafetyEye Streamlit Dashboard Demo (No Model Required)
# # app_demo.py

# import streamlit as st
# import cv2
# import numpy as np
# import pandas as pd
# import time
# from datetime import datetime
# from PIL import Image
# import io
# import random

# st.set_page_config(page_title="SafetyEye - Demo Dashboard", layout="wide")

# st.sidebar.title("SafetyEye (Demo)")
# mode = st.sidebar.selectbox("Mode", ["Simulator (no model)", "Upload images/videos (test)", "Connect model (placeholder)"])
# sim_people = st.sidebar.slider("Simulated people per frame", 1, 10, 3)
# sim_violation_rate = st.sidebar.slider("Simulated violation rate (%)", 0, 100, 20)
# show_boxes = st.sidebar.checkbox("Show bounding boxes in demo", True)
# start = st.sidebar.button("Start")
# stop = st.sidebar.button("Stop")
# clear_logs = st.sidebar.button("Clear logs")

# uploaded_file = None
# if mode == "Upload images/videos (test)":
#     uploaded_file = st.sidebar.file_uploader("Upload image or short video (mp4)", type=["jpg","jpeg","png","mp4","mov","avi"])

# model_path = st.sidebar.text_input("Model path (when ready)", "best.pt")

# if "running" not in st.session_state:
#     st.session_state.running = False
# if "logs" not in st.session_state:
#     st.session_state.logs = []

# if start:
#     st.session_state.running = True
# if stop:
#     st.session_state.running = False
# if clear_logs:
#     st.session_state.logs = []

# col1, col2 = st.columns([2,1])
# with col1:
#     st.header("Live / Demo Feed")
#     feed_slot = st.empty()
# with col2:
#     st.header("Safety Metrics")
#     people_metric = st.metric("People detected", 0)
#     viol_metric = st.metric("Violations (current)", 0)
#     tot_alerts = st.metric("Total alerts (session)", 0)
#     st.subheader("Violation Log")
#     log_slot = st.empty()
#     st.download_button("Export logs CSV (current session)", data="", key="download", help="Export will be enabled once logs exist")

# st.markdown("---")
# st.caption("Mode: " + mode)

# def simulate_frame(frame_id, people_count, violation_rate):
#     h, w = 480, 720
#     frame = np.ones((h,w,3), dtype=np.uint8) * 200
#     detections = []
#     for i in range(people_count):
#         x1 = int((i+0.1)*w/(people_count+1)) - 30
#         y1 = random.randint(120, 220)
#         x2 = x1 + random.randint(50, 90)
#         y2 = y1 + random.randint(120, 180)
#         x1, x2 = max(5,x1), min(w-5,x2)

#         missing = []
#         if random.random() < violation_rate/100.0:
#             missing = random.choice([["helmet"], ["vest"], ["helmet","vest"]])

#         cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), -1)
#         cv2.circle(frame, (int((x1+x2)/2), y1-15), 15, (100,150,200), -1)

#         if "helmet" not in missing:
#             cv2.rectangle(frame, (x1, y1-40), (x2, y1-22), (0,255,0), -1)
#         else:
#             cv2.rectangle(frame, (x1, y1-40), (x2, y1-22), (0,0,255), 2)

#         if "vest" not in missing:
#             cv2.rectangle(frame, (x1+5, int(y1+20)), (x2-5, y1+70), (0,255,0), -1)
#         else:
#             cv2.rectangle(frame, (x1+5, int(y1+20)), (x2-5, y1+70), (0,0,255), 2)

#         detections.append({"person_id": i, "bbox":(x1,y1,x2,y2), "missing": missing})

#         if show_boxes:
#             color = (0,255,0) if not missing else (0,0,255)
#             cv2.rectangle(frame,(x1,y1),(x2,y2), color, 2)
#             cv2.putText(frame, f"P{i}", (x1, y1-50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     return frame_rgb, detections

# frame_id = 0
# if st.session_state.running:
#     if mode == "Simulator (no model)":
#         st.info("Running simulator mode — no model needed.")
#         while st.session_state.running:
#             frame_id += 1
#             frame, dets = simulate_frame(frame_id, sim_people, sim_violation_rate)

#             for d in dets:
#                 if d["missing"]:
#                     entry = {
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                         "frame_id": frame_id,
#                         "person_id": d["person_id"],
#                         "missing": ",".join(d["missing"]),
#                     }
#                     st.session_state.logs.append(entry)

#             feed_slot.image(frame, use_column_width=True)
#             people_metric.metric("People detected", len(dets))
#             viol_metric.metric("Violations (current)", sum(1 for d in dets if d["missing"]))
#             tot_alerts.metric("Total alerts (session)", len(st.session_state.logs))

#             if st.session_state.logs:
#                 df = pd.DataFrame(st.session_state.logs)
#                 log_slot.dataframe(df.tail(20))
#                 csv = df.to_csv(index=False).encode("utf-8")
#                 st.download_button("Export logs CSV", data=csv,
#                                    file_name="safeteye_logs.csv",
#                                    mime="text/csv", key=f"dl_{time.time()}")

#             time.sleep(0.5)
#     else:
#         st.warning("Only simulator mode is implemented right now.")

# else:
#     st.info("Press Start to begin the dashboard.")


########################################################################################################################################################


#streamlit run app_demo.py
#

import os
import time
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime

import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import io

# ---------------- Page config ----------------
st.set_page_config(page_title="SafetyEye - Demo (Email Alerts)", layout="wide")

# ---------------- Sidebar: Controls ----------------
st.sidebar.title("SafetyEye (Demo)")
mode = st.sidebar.selectbox("Mode", ["Simulator (no model)", "Upload images/videos (test)", "Connect model (placeholder)"])
sim_people = st.sidebar.slider("Simulated people per frame", 1, 10, 3)
sim_violation_rate = st.sidebar.slider("Simulated violation rate (%)", 0, 100, 20)
show_boxes = st.sidebar.checkbox("Show bounding boxes in demo", True)

start = st.sidebar.button("Start")
stop = st.sidebar.button("Stop")
clear_logs = st.sidebar.button("Clear logs")

# Upload control for testing images/videos
uploaded_file = None
if mode == "Upload images/videos (test)":
    uploaded_file = st.sidebar.file_uploader("Upload image or short video (mp4)", type=["jpg","jpeg","png","mp4","mov","avi"])

model_path = st.sidebar.text_input("Model path (when ready)", "best.pt")

# ---------------- Email settings ----------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Email Alert Settings")
email_enabled = st.sidebar.checkbox("Enable email alerts", value=False)
smtp_host = st.sidebar.text_input("SMTP host", value=os.getenv("SMTP_HOST", "smtp.gmail.com"))
smtp_port = st.sidebar.number_input("SMTP port", value=int(os.getenv("SMTP_PORT", 465)), step=1)
smtp_user = st.sidebar.text_input("Sender email", value=os.getenv("SMTP_USER", ""))
smtp_password = st.sidebar.text_input("SMTP password / app password", value=os.getenv("SMTP_PASS", ""), type="password")
recipients_text = st.sidebar.text_input("Recipient emails (comma separated)", value=os.getenv("ALERT_RECIPIENTS", ""))
try:
    recipients = [e.strip() for e in recipients_text.split(",") if e.strip()]
except:
    recipients = []
email_cooldown_sec = st.sidebar.number_input("Email cooldown (s)", value=60, min_value=5, step=5)
st.sidebar.markdown("---")
st.sidebar.caption("For Gmail: use App Passwords (requires 2FA).")

# ---------------- Session state initialization ----------------
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []  # each entry: timestamp, frame_id, person_id, missing
if "last_email_times" not in st.session_state:
    st.session_state.last_email_times = {}  # vkey -> epoch seconds

if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False
if clear_logs:
    st.session_state.logs = []
    st.session_state.last_email_times = {}

# ---------------- Layout ----------------
col1, col2 = st.columns([2, 1])
with col1:
    st.header("Live / Demo Feed")
    feed_slot = st.empty()
with col2:
    st.header("Safety Metrics")
    people_metric = st.metric("People detected", 0)
    viol_metric = st.metric("Violations (current)", 0)
    tot_alerts = st.metric("Total alerts (session)", 0)
    st.subheader("Violation Log")
    log_slot = st.empty()
    # download button will be updated when logs exist
    st.download_button("Export logs CSV (current session)", data="", key="download", help="Export will be enabled once logs exist")

st.markdown("---")
st.caption(f"Mode: {mode}")

# ---------------- Helper: Email sender ----------------
def send_email_alert(smtp_host, smtp_port, smtp_user, smtp_password,
                     subject, body, to_addrs, use_ssl=True):
    """
    Send an email alert. Returns True on success, False on failure.
    """
    try:
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = ", ".join(to_addrs) if isinstance(to_addrs, (list, tuple)) else to_addrs
        msg["Subject"] = subject
        msg.set_content(body)

        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.ehlo()
            server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        # keep UI non-fatal; print to console for debugging
        print("Email send failed:", e)
        return False

# ---------------- Helper: Simulate frame ----------------
def simulate_frame(frame_id, people_count, violation_rate):
    h, w = 480, 720
    frame = np.ones((h, w, 3), dtype=np.uint8) * 200
    detections = []
    for i in range(people_count):
        # simple arranged placement so visuals look tidy
        x1 = int((i + 0.1) * w / (people_count + 1)) - 30
        y1 = random.randint(120, 220)
        x2 = x1 + random.randint(50, 90)
        y2 = y1 + random.randint(120, 180)
        x1, x2 = max(5, x1), min(w - 5, x2)

        missing = []
        if random.random() < violation_rate / 100.0:
            missing = random.choice([["helmet"], ["vest"], ["helmet", "vest"]])

        # draw person (rectangle body + circle head)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), -1)
        cv2.circle(frame, (int((x1 + x2) / 2), y1 - 15), 15, (100, 150, 200), -1)

        # helmet indicator
        if "helmet" not in missing:
            cv2.rectangle(frame, (x1, y1 - 40), (x2, y1 - 22), (0, 255, 0), -1)
        else:
            cv2.rectangle(frame, (x1, y1 - 40), (x2, y1 - 22), (0, 0, 255), 2)

        # vest indicator
        if "vest" not in missing:
            cv2.rectangle(frame, (x1 + 5, int(y1 + 20)), (x2 - 5, y1 + 70), (0, 255, 0), -1)
        else:
            cv2.rectangle(frame, (x1 + 5, int(y1 + 20)), (x2 - 5, y1 + 70), (0, 0, 255), 2)

        detections.append({"person_id": i, "bbox": (x1, y1, x2, y2), "missing": missing})

        if show_boxes:
            color = (0, 255, 0) if not missing else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"P{i}", (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, detections

# ---------------- Helper: Process uploaded media (basic) ----------------
def process_uploaded_frame(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb

# ---------------- Main loop ----------------
frame_id = 0
if st.session_state.running:
    if mode == "Simulator (no model)":
        st.info("Running simulator mode — no model needed.")
        while st.session_state.running:
            frame_id += 1
            frame, dets = simulate_frame(frame_id, sim_people, sim_violation_rate)

            # For each detection that has missing PPE, create log and optionally send email
            for d in dets:
                if d["missing"]:
                    entry = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "frame_id": frame_id,
                        "person_id": d["person_id"],
                        "missing": ",".join(d["missing"]),
                    }
                    st.session_state.logs.append(entry)

                    # Email alert handling (per missing item, with cooldown)
                    if email_enabled and smtp_user and smtp_password and recipients:
                        for item in d["missing"]:
                            vkey = f"person_{d['person_id']}_{item}"
                            last = st.session_state.last_email_times.get(vkey, 0)
                            now_ts = time.time()
                            if now_ts - last >= email_cooldown_sec:
                                subject = f"[SafetyEye] Violation: missing {item}"
                                body = (
                                    f"Time: {entry['timestamp']}\n"
                                    f"Frame: {entry['frame_id']}\n"
                                    f"Person ID: {entry['person_id']}\n"
                                    f"Missing: {item}\n\n"
                                    "This is an automated alert from SafetyEye (demo)."
                                )
                                success = send_email_alert(
                                    smtp_host=smtp_host,
                                    smtp_port=smtp_port,
                                    smtp_user=smtp_user,
                                    smtp_password=smtp_password,
                                    subject=subject,
                                    body=body,
                                    to_addrs=recipients,
                                    use_ssl=(smtp_port == 465),
                                )
                                if success:
                                    st.session_state.last_email_times[vkey] = now_ts
                                    print(f"Email sent for {vkey} to {recipients}")
                                else:
                                    print("Failed to send email for", vkey)

            # Update UI
            feed_slot.image(frame, use_column_width=True)
            people_metric.metric("People detected", len(dets))
            viol_metric.metric("Violations (current)", sum(1 for d in dets if d["missing"]))
            tot_alerts.metric("Total alerts (session)", len(st.session_state.logs))

            if st.session_state.logs:
                df = pd.DataFrame(st.session_state.logs)
                log_slot.dataframe(df.tail(20))
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Export logs CSV", data=csv,
                                   file_name="safeteye_logs.csv",
                                   mime="text/csv",
                                   key=f"dl_{time.time()}")

            time.sleep(0.6)

    elif mode == "Upload images/videos (test)":
        st.info("Upload mode — use the upload control in the sidebar.")
        if uploaded_file is None:
            st.warning("Upload an image or short video to start testing. For video, only short clips are recommended.")
            st.session_state.running = False
        else:
            file_bytes = uploaded_file.read()
            file_ext = uploaded_file.name.split(".")[-1].lower()
            if file_ext in ("jpg", "jpeg", "png"):
                img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                frame = np.array(img)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                proc = process_uploaded_frame(frame_bgr)
                feed_slot.image(proc, use_column_width=True)
                if st.button("Log violation for this frame (manual)"):
                    # simple manual log entry
                    missing_text = st.text_input("Enter missing PPE (comma separated)", value="helmet")
                    if missing_text:
                        entry = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "frame_id": 1,
                            "person_id": None,
                            "missing": missing_text,
                        }
                        st.session_state.logs.append(entry)
            else:
                with open("temp_upload.mp4", "wb") as f:
                    f.write(file_bytes)
                cap = cv2.VideoCapture("temp_upload.mp4")
                st.info("Playing uploaded video (press Stop in sidebar to stop).")
                while st.session_state.running and cap.isOpened():
                    ret, fr = cap.read()
                    if not ret:
                        break
                    frame_id += 1
                    rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
                    feed_slot.image(rgb, use_column_width=True)
                    time.sleep(0.05)
                cap.release()
            # update logs UI after upload processed
            if st.session_state.logs:
                df = pd.DataFrame(st.session_state.logs)
                log_slot.dataframe(df.tail(20))
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Export logs CSV", data=csv, file_name="safeteye_logs.csv", mime="text/csv", key="dl2")
            st.session_state.running = False

    else:
        st.warning("Connect model placeholder – model integration not implemented in demo.")
        st.session_state.running = False

else:
    st.info("Press Start to begin the dashboard.")
