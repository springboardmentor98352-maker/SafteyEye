import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import time
from email_alert import send_email_alert
from PIL import Image
import pandas as pd
import os

# ---------------------------
# Load Model
# ---------------------------
MODEL_PATH = "runs/detect/construction_ppe_model/weights/best.pt"
model = YOLO(MODEL_PATH)

CSV_FILE = "violation_logs.csv"

# ---------------------------
# Session State Init
# ---------------------------
if "last_email_time" not in st.session_state:
    st.session_state.last_email_time = 0

if "violation_log" not in st.session_state:
    # Load existing CSV data if available
    if os.path.exists(CSV_FILE):
        st.session_state.violation_log = pd.read_csv(CSV_FILE).to_dict("records")
    else:
        st.session_state.violation_log = []

EMAIL_INTERVAL = 60  # seconds

# ---------------------------
# Class Info
# ---------------------------
CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle"
]

VIOLATION_CLASSES = {
    2: "NO-Hardhat",
    3: "NO-Mask",
    4: "NO-Safety Vest"
}

# ---------------------------
# Streamlit UI Setup
# ---------------------------
st.set_page_config(page_title="SafetyEye PPE Detection", layout="wide")
st.title("🦺 SafetyEye – PPE Detection & Safety Analytics System")
st.write("AI-powered system to detect PPE violations with alerts and analytics.")

option = st.sidebar.selectbox(
    "Select Mode",
    ("Image Detection", "Video Detection", "Webcam (Live Detection)")
)

conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.35)

# ---------------------------
# Helper Functions
# ---------------------------
def annotate_image(result):
    img = result.plot()
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def check_violations(result):
    violations = []
    if result.boxes:
        classes = result.boxes.cls.cpu().numpy().astype(int)
        for cls in classes:
            if cls in VIOLATION_CLASSES:
                violations.append(VIOLATION_CLASSES[cls])
    return violations

def log_and_alert(violations):
    current_time = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    if violations:
        # Log violation
        st.session_state.violation_log.append({
            "Time": timestamp,
            "Violations": ", ".join(violations)
        })

        # Save to CSV (PERMANENT STORAGE)
        df = pd.DataFrame(st.session_state.violation_log)
        df.to_csv(CSV_FILE, index=False)

        # Email cooldown
        if current_time - st.session_state.last_email_time > EMAIL_INTERVAL:
            send_email_alert(", ".join(violations))
            st.session_state.last_email_time = current_time

# ---------------------------
# IMAGE MODE
# ---------------------------
if option == "Image Detection":
    st.header("📷 Image PPE Detection")

    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Image", width=500)

        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        results = model.predict(img_cv, conf=conf_threshold)

        annotated = annotate_image(results[0])
        violations = check_violations(results[0])
        log_and_alert(violations)

        st.subheader("🔍 Detection Result")
        st.image(annotated, use_column_width=True)

        if violations:
            st.error("⚠️ Violations Detected")
            for v in violations:
                st.write("- " + v)
        else:
            st.success("✅ No PPE Violations Detected!")

# ---------------------------
# VIDEO MODE
# ---------------------------
elif option == "Video Detection":
    st.header("🎞 Video PPE Detection")

    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if uploaded_video:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())

        st.info("Processing video...")

        cap = cv2.VideoCapture(tfile.name)
        last_result = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = model.predict(frame, conf=conf_threshold, verbose=False)
            last_result = results[0]

        cap.release()

        if last_result:
            annotated = annotate_image(last_result)
            violations = check_violations(last_result)
            log_and_alert(violations)

            st.success("Video Processed Successfully")
            st.image(annotated, use_column_width=True)

# ---------------------------
# WEBCAM MODE
# ---------------------------
elif option == "Webcam (Live Detection)":
    st.header("🎥 Webcam Live PPE Detection")
    st.warning("Run from terminal. Press Q to quit webcam window.")

    run_webcam = st.button("Start Webcam")

    if run_webcam:
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(frame, conf=conf_threshold, verbose=False)
            annotated = results[0].plot()
            violations = check_violations(results[0])
            log_and_alert(violations)

            cv2.imshow("SafetyEye Live Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# ---------------------------
# DASHBOARD & ANALYTICS
# ---------------------------
st.markdown("---")
st.header("📊 Safety Compliance Analytics")

if st.session_state.violation_log:
    df = pd.DataFrame(st.session_state.violation_log)

    st.subheader("🗂 Violation Logs")
    st.dataframe(df)

    st.subheader("📈 Violation Distribution")
    violation_counts = (
        df["Violations"]
        .str.split(", ")
        .explode()
        .value_counts()
    )
    st.bar_chart(violation_counts)

    st.subheader("📉 Violation Trend Over Time")
    time_series = df.groupby("Time").size()
    st.line_chart(time_series)

    st.download_button(
        "⬇️ Download Violation Logs (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        "safety_violation_logs.csv",
        "text/csv"
    )
else:
    st.info("No violations recorded yet.")
