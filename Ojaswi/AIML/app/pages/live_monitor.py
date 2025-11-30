import streamlit as st
import cv2
import time
from datetime import datetime
from pathlib import Path
import json

# your backend helpers
from app.backend.detector import predict_frame, save_violation
from app.backend.utils import generate_pdf

# email alert safe import
try:
    from app.backend.email_alert import send_email_alert
    EMAIL_OK = True
except Exception as e:
    EMAIL_OK = False
    EMAIL_ERR = str(e)


# ==============================================
# Load Settings
# ==============================================
def load_settings():
    file = Path("database/settings.json")

    if file.exists():
        try:
            return json.loads(file.read_text())
        except:
            pass

    return {
        "confidence_threshold": 0.35,
        "audio_alerts": True,
        "generate_pdf": True,
        "sender": "",
        "receiver": "",
        "app_pass": "",
        "cooldown_seconds": 8   # default
    }


# ==============================================
# Streamlit Page
# ==============================================
def app():

    st.subheader("🚨 Live AI Monitoring")
    st.caption("🛡️ Helmet | Mask | Vest | PPE Violation Detection & Auto Logging / PDF / Email Alert")

    if not EMAIL_OK:
        st.warning(f"⚠️ Email alert module not loaded: {EMAIL_ERR}")

    settings = load_settings()

    cooldown_limit = int(settings.get("cooldown_seconds", 8))

    # Camera option
    mode = st.radio("📷 Select Camera Source:", ["🎥 Local Webcam"], horizontal=True)

    col1, col2 = st.columns([4, 1])

    # ============================================
    # LEFT SIDE — LIVE FEED
    # ============================================
    with col1:

        frame_placeholder = st.empty()
        alert_box = st.empty()
        fps_box = st.empty()

        # Buttons
        start_btn = st.button("▶ Start Detection")
        stop_btn = st.button("⛔ Stop Detection")

        running = False

        if start_btn:
            running = True

        if stop_btn:
            running = False

        if running:

            # open webcam
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not cap.isOpened():
                st.error("❌ Unable to access webcam.")
                return

            last_detect_time = 0
            last_frame_time = time.time()

            st.success("🟢 Monitoring Started...")

            while running:

                ret, frame = cap.read()
                if not ret:
                    st.error("⚠️ Frame not received.")
                    break

                # YOLO Prediction
                try:
                    results = predict_frame(frame)
                except Exception as e:
                    st.error(f"❌ Model error: {e}")
                    break

                annotated = results.plot()

                # FPS
                now = time.time()
                fps = 1 / (now - last_frame_time)
                last_frame_time = now
                fps_box.write(f"📡 FPS: **{fps:.2f}**")

                # Check detections
                for det in results.boxes:

                    cls = results.names[int(det.cls[0])]
                    conf = float(det.conf[0])

                    if conf < settings["confidence_threshold"]:
                        continue

                    # Cooldown
                    if (now - last_detect_time) < cooldown_limit:
                        continue

                    last_detect_time = now

                    # Save Violation
                    fname, vid, timestamp = save_violation(cls, conf, frame)

                    # PDF
                    pdf_path = None
                    if settings.get("generate_pdf", True):
                        pdf_path = generate_pdf(vid, cls, fname, timestamp, conf)

                    # Email Alert
                    if EMAIL_OK and settings.get("sender") and settings.get("receiver"):
                        try:
                            send_email_alert(
                                receiver_email=settings["receiver"],
                                subject=f"🚨 {cls} Violation Detected",
                                body=f"""
A violation was detected.

📌 Type: {cls}
⏰ Time: {timestamp}
🎯 Confidence: {conf:.2f}

PDF report attached if enabled.
""",
                                attachment_path=pdf_path,
                                sender_email=settings["sender"],
                                app_password=settings["app_pass"]
                            )
                            alert_box.success("📧 Email sent successfully!")
                        except Exception as e:
                            alert_box.warning(f"⚠️ Email failed: {e}")

                    # On-screen alert
                    alert_box.markdown(
                        f"""
                        <div style="padding:10px;background:#ef4444;color:white;border-radius:8px;">
                        🚨 <b>{cls}</b> detected — Confidence {conf:.2f}<br>
                        📅 Logged at {timestamp}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Beep sound
                    if settings.get("audio_alerts", True):
                        beep = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YQAAAAA="
                        st.markdown(
                            f"<audio autoplay><source src='data:audio/wav;base64,{beep}'/></audio>",
                            unsafe_allow_html=True
                        )

                # Show Stream
                frame_placeholder.image(annotated, channels="BGR")

                # Stop check
                if st.button("⛔ Stop Detection"):
                    running = False
                    break

            cap.release()
            st.success("🛑 Monitoring Stopped.")


    # ============================================
    # RIGHT SIDE — CONTROLS DISPLAY
    # ============================================
    with col2:
        st.markdown("### ⚙️ Detection Controls")
        st.write(f"🎯 Confidence Threshold: `{settings['confidence_threshold']}`")
        st.write(f"🔔 Audio Alerts: `{settings['audio_alerts']}`")
        st.write(f"📄 PDF Auto Generate: `{settings['generate_pdf']}`")
        st.write(f"⏱ Cooldown (s): `{cooldown_limit}`")
        st.write("---")
        st.write("### 📧 Email Settings")
        st.write(f"✉️ Sender: `{settings.get('sender','Not Set')}`")
        st.write(f"📥 Receiver: `{settings.get('receiver','Not Set')}`")
