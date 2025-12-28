import streamlit as st
import cv2
import pandas as pd
from pathlib import Path
from app.backend.detector import detect_violations, count_people, save_violation

st.set_page_config(page_title="Live PPE Monitoring", layout="wide")

# ---------------- CSV LOGGING ----------------
def append_to_csv(vid, violations, img_path, timestamp):
    csv_path = Path("database/violations_log.csv")
    df_new = pd.DataFrame([{
        "id": vid,
        "label": ",".join(violations),
        "confidence": 1.0,
        "image": img_path,
        "timestamp": timestamp
    }])
    if csv_path.exists():
        df_new.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df_new.to_csv(csv_path, index=False)

# ---------------- MAIN APP ----------------
def app():
    st.subheader("🚨 Live PPE Monitoring")

    col1, col2 = st.columns([3, 1])
    frame_box = col1.empty()
    stats_box = col2.empty()

    start = st.button("▶ Start Detection")
    stop = st.button("⛔ Stop Detection")

    if start:
        cap = cv2.VideoCapture(0)
        running = True

        total_frames = 0
        total_violations = 0

        st.success("🟢 Monitoring Started")

        while running:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Failed to read from camera")
                break

            total_frames += 1

            # ---------------- DETECTION ----------------
            violations, results = detect_violations(frame)
            annotated = results.plot()
            frame_box.image(annotated, channels="BGR")

            people = count_people(results)

            # ---------------- SAVE VIOLATION ----------------
            if violations:
                img_path, vid, timestamp = save_violation(violations, frame)
                if img_path:
                    append_to_csv(vid, violations, img_path, timestamp)
                    total_violations += 1

            # ---------------- STATS ----------------
            stats_box.markdown(f"""
            ### 📊 Analytics
            👥 People Detected: **{people}**  
            🚨 Violations Today: **{total_violations}**
            """)

            if stop:
                running = False
                break

        cap.release()
        st.success("🛑 Monitoring Stopped")
