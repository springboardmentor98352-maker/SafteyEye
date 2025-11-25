import streamlit as st
import cv2
import time
from datetime import datetime
from pathlib import Path
import json

from app.backend.detector import predict_frame, save_violation
from app.backend.utils import generate_pdf
try:
    from app.backend.email_alert import send_email_alert
except:
    st.error("❌ Missing file: app/backend/email_alert.py")



# Load stored settings
def load_settings():
    settings_file = Path("database/settings.json")
    if settings_file.exists():
        return json.loads(settings_file.read_text())
    return {
        "confidence_threshold": 0.35,
        "audio_alerts": True,
        "generate_pdf": True,
        "sender": "",
        "receiver": "",
        "app_pass": ""
    }


def app():

    st.subheader("🚨 Live AI Monitoring")
    st.caption("Helmet | Mask | Vest | PPE Violation Detection & Auto Logging / PDF / Email Alert")

    settings = load_settings()

    mode = st.radio("Camera Source:", ["Local Webcam", "RTSP / IP Camera"], horizontal=True)

    rtsp_url = None
    if mode == "RTSP / IP Camera":
        rtsp_url = st.text_input("Enter RTSP Stream URL:", "rtsp://")

    col1, col2 = st.columns([4, 1])

    # ----------------------------- Left Panel: Live Feed -----------------------------

    with col1:
        st_frame = st.empty()
        alert_box = st.empty()
        fps_display = st.empty()

        start_btn = st.button("▶ Start Detection")
        stop_btn = st.button("⛔ Stop")

        if start_btn and not stop_btn:

            source = 0 if mode == "Local Webcam" else rtsp_url
            cap = cv2.VideoCapture(source)
            prev_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("❌ Camera not accessible")
                    break

                results = predict_frame(frame)
                annotated = results.plot()

                # FPS Calculation
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time
                fps_display.write(f"🎥 FPS: {fps:.2f}")

                # ------------------- Scan detections -------------------
                for det in results.boxes:
                    cls = results.names[int(det.cls[0])]
                    conf = float(det.conf[0])

                    # Check confidence threshold (from Settings)
                    if conf < settings["confidence_threshold"]:
                        continue

                    # Save violation
                    fname, vid, timestamp = save_violation(cls, conf, frame)

                    # ------------------- Generate PDF if enabled -------------------
                    pdf_path = None
                    if settings.get("generate_pdf", True):
                        pdf_path = generate_pdf(vid, cls, fname, timestamp, conf)

                    # ------------------- Email Alert if configured -------------------
                    if settings.get("receiver") and settings.get("sender") and settings.get("app_pass"):
                        send_email_alert(
                            receiver_email=settings["receiver"],
                            subject=f"🚨 {cls} Violation Detected",
                            body=f"""
A violation was detected.

📌 Type: {cls}
📆 Time: {timestamp}
🎯 Confidence: {conf:.2f}

PDF report attached if enabled.
                            """,
                            attachment_path=pdf_path,
                            sender_email=settings["sender"],
                            app_password=settings["app_pass"]
                        )

                    # ------------------- Live UI Alert -------------------
                    alert_box.markdown(
                        f"""
                        <div style="padding:10px;border-radius:8px;background:#ff0033;color:white;">
                        🚨 <strong>{cls}</strong> detected (Confidence: {conf:.2f}) <br>
                        Logged at {timestamp}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ------------------- Play Beep if enabled -------------------
                    if settings.get("audio_alerts", True):
                        beep = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YQAAAAA="
                        st.markdown(
                            f"<audio autoplay><source src='data:audio/wav;base64,{beep}'/></audio>",
                            unsafe_allow_html=True
                        )

                # Stream
                st_frame.image(annotated, channels="BGR")

                if stop_btn:
                    break

            cap.release()
            st.success("🛑 Detection stopped.")


    # ----------------------------- Right Panel Controls -----------------------------

    with col2:
        st.markdown("### ⚙ Detection Controls")
        st.write(f"📍 Confidence Threshold: `{settings['confidence_threshold']}`")
        st.write(f"🔔 Alerts Enabled: `{settings['audio_alerts']}`")
        st.write(f"📄 PDF Auto-Generate: `{settings['generate_pdf']}`")
        st.write("---")
        st.write("📧 Email Notifications:")
        st.write(f"Sender: `{settings.get('sender','Not Set')}`")
        st.write(f"Receiver: `{settings.get('receiver','Not Set')}`")


    st.markdown("---")
    st.info("Violations will appear automatically on the Reports page.")

