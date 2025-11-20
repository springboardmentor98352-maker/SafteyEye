import streamlit as st
import cv2
from ultralytics import YOLO
import time
import numpy as np
import tempfile
import os


# Load model
model = YOLO("C:/Users/PRANITHA/OneDrive/Desktop/Safetyeye/models/best.pt")


# Function to check PPE violations
def check_violations(result):
    names = result.names
    classes = result.boxes.cls.tolist()

    violations = []
    detected = [names[int(c)] for c in classes]

    if "Person" in detected:
        if "No_Hardhat" in detected:
            violations.append("Worker without Helmet")
        if "No_Vest" in detected:
            violations.append("Worker without Safety Vest")
        if "No_Gloves" in detected:
            violations.append("Worker without Gloves")

    return violations


# Streamlit UI Title
st.title("SafetyEye Dashboard")
st.subheader("Real-time PPE Violation Monitoring")


# File upload box for video
uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_video:

    # Save uploaded file to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_video.read())
    video_path = temp_file.name

    st.write("Video uploaded successfully")

    # Placeholders for UI elements
    video_display = st.empty()
    violations_box = st.empty()
    total_counter_box = st.empty()

    total_violations = 0
    history = []

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO prediction
        results = model.predict(frame, conf=0.5)

        # Annotated frame
        annotated_frame = results[0].plot()

        # Convert BGR to RGB for Streamlit
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        # Check for violations
        violations = check_violations(results[0])

        if violations:
            total_violations += 1
            history.append(violations)

        # Show video frame on dashboard
        video_display.image(annotated_frame, caption="Live Analysis", use_container_width=True)

        # Show current violation list
        if violations:
            violations_box.warning(f"Current Violations: {violations}")
        else:
            violations_box.info("No violations detected")

        # Show total violations count
        total_counter_box.write(f"Total Violations Detected: {total_violations}")

        time.sleep(0.03)

    cap.release()
    os.unlink(video_path)

    st.success("Video processing completed")
    st.write("Violation History:")
    st.write(history)
