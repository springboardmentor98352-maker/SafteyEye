# app/pages/live_monitor.py
import streamlit as st
import cv2
import base64
from datetime import datetime
import time
from app.backend.detector import predict_frame, save_violation

def app():
    st.header("🚨 Live Traffic Enforcement — AI Detection")
    st.markdown("Real-time Helmet, Mask, Vest, Person compliance with auto-logging & alerts.")

    mode = st.radio("Select Camera Source:", ["Local Webcam", "RTSP / IP Camera"], horizontal=True)

    if mode == "RTSP / IP Camera":
        rtsp = st.text_input("RTSP / IP Camera URL", "rtsp://")
    else:
        rtsp = None

    col1, col2 = st.columns([4, 1])

    # ------------------------------------------
    # LEFT — Live Video Feed with Detection
    # ------------------------------------------
    with col1:
        st_frame = st.empty()
        fps_display = st.empty()
        alert_area = st.empty()

        start = st.button("▶ Start Live Detection")
        stop_flag = st.button("⛔ Stop Detection")

        if start and not stop_flag:
            # source selection
            source = 0 if mode == "Local Webcam" else rtsp

            cap = cv2.VideoCapture(source)

            prev_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("❌ Unable to access camera")
                    break

                # YOLO detection
                results = predict_frame(frame)
                annotated = results.plot()

                # FPS calculation
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time

                fps_display.markdown(f"**FPS:** {fps:.2f}")

                # Scan detections
                for det in results.boxes:
                    cls = results.names[int(det.cls[0])]
                    conf = float(det.conf[0])

                    # Flag violations
                    if cls in ["NO-Hardhat", "NO-Mask", "NO-Vest"]:
                        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Save violation evidence
                        fname, vid, timestamp = save_violation(cls, conf, frame)

                        # LIVE ALERT UI
                        alert_area.markdown(
                            f"""
                            <div style='padding:10px;background:#8b1c3a;color:white;border-radius:8px;'>
                                🚨 <b>{cls}</b> detected — {timestamp}<br>
                                Evidence saved: {fname}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Play alert sound
                        beep = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YQAAAAA="
                        st.markdown(
                            f"<audio autoplay><source src='data:audio/wav;base64,{beep}' /></audio>",
                            unsafe_allow_html=True,
                        )

                # Stream on UI
                st_frame.image(annotated, channels="BGR")

                if stop_flag:
                    break

            cap.release()
            st.success("🔴 Live detection stopped.")

    # ------------------------------------------
    # RIGHT — Control Panel
    # ------------------------------------------
    with col2:
        st.markdown("### ⚙ Controls")
        st.slider("Confidence Threshold", 0.0, 1.0, 0.35, 0.01)

        st.markdown("### 🔔 Alert Settings")
        st.checkbox("Enable Audio Alerts", True)
        st.checkbox("Flash Screen on Violation", True)

        st.markdown("### 🚓 Manual Quick Report")
        v_type = st.selectbox("Violation", ["NO-Helmet", "NO-Mask", "NO-Vest", "Overspeed", "Signal Jump"])
        loc = st.text_input("Location")
        phone = st.text_input("Phone Number")

        if st.button("Add Manual Violation"):
            st.success(f"Violation logged: {v_type} at {loc} | Notify {phone}")

    st.markdown("---")
    st.info("All violations are saved automatically and visible on the Reports page.")
