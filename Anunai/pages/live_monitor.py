"""
pages/live_monitor.py

Live Monitor page:
- Runs the simulator (demo mode)
- Logs frame summaries + per-violation rows to storage
- Supports safe email alerts (optional)
- No Streamlit secrets required — uses fallback system
"""

import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

from core.inference import simulate_frame   # simulator
from core.rules import detect_violations    # rule engine
from core import storage, emailer           # logging + email


# ---------------------------------------------------------------------
# SAFE SECRET / ENV ACCESS FUNCTION
# ---------------------------------------------------------------------
def get_secret_or_env(key: str, default=""):
    """
    Safely returns secret → environment → default.
    Avoids StreamlitSecretNotFoundError.
    """
    # Try Streamlit secrets (protected)
    try:
        if hasattr(st, "secrets"):
            val = st.secrets.get(key)
            if val not in (None, ""):
                return val
    except Exception:
        pass

    # Try environment variables
    env_val = os.environ.get(key)
    if env_val not in (None, ""):
        return env_val

    # Fallback default
    return default


# ---------------------------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------------------------
def app():
    st.title("Live Monitor")
    st.caption("Live demo feed. Use Start/Stop from the sidebar to control the simulator.")

    # -----------------------------------------------------------------
    # Layout: left video feed / right controls
    # -----------------------------------------------------------------
    col_left, col_right = st.columns([2, 1])

    # ---------------- Video feed area ----------------
    with col_left:
        feed_slot = st.empty()

    # ---------------- Simulation & Email Controls ----------------
    with col_right:
        st.subheader("Simulation controls")
        people_count = st.number_input("Simulated people per frame",
                                       min_value=1, max_value=10, value=3)
        violation_rate = st.slider("Violation rate (%)", 0, 100, 20)
        show_boxes = st.checkbox("Show bounding boxes", True)

        st.markdown("---")
        st.subheader("Email Alerts (optional)")

        enable_email = st.checkbox("Enable email alerts", value=False)

        smtp_host = st.text_input(
            "SMTP host",
            value=get_secret_or_env("SMTP_HOST", "smtp.gmail.com")
        )
        smtp_port = st.number_input(
            "SMTP port",
            value=int(get_secret_or_env("SMTP_PORT", 465)),
            step=1
        )
        smtp_user = st.text_input(
            "Sender email",
            value=get_secret_or_env("SMTP_USER", "")
        )
        smtp_password = st.text_input(
            "SMTP password / app password",
            value=get_secret_or_env("SMTP_PASS", ""),
            type="password"
        )
        recipients_raw = st.text_input(
            "Recipient emails (comma separated)",
            value=get_secret_or_env("ALERT_RECIPIENTS", "")
        )
        recipients = [x.strip() for x in recipients_raw.split(",") if x.strip()]

        email_cooldown = int(get_secret_or_env("EMAIL_COOLDOWN", 60))
        email_cooldown = st.number_input(
            "Email cooldown (s)",
            value=email_cooldown,
            min_value=5,
            step=5
        )

    # ---------------------------------------------------------------------
    # SESSION STATE (global control created in app.py)
    # ---------------------------------------------------------------------
    if "running" not in st.session_state:
        st.session_state.running = False
    if "last_email_times" not in st.session_state:
        st.session_state.last_email_times = {}

    # ---------------------------------------------------------------------
    # MAIN LOOP (runs only while Start is active)
    # ---------------------------------------------------------------------
    frame_id = 0

    while st.session_state.running:
        frame_id += 1

        # Create a simulated frame
        frame_rgb, detections = simulate_frame(
            frame_id,
            people_count=people_count,
            violation_rate=violation_rate,
            show_boxes=show_boxes
        )

        # Detect violations through rules engine
        violations = detect_violations(detections)

        # Timestamp
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ---------------- Save FRAME SUMMARY row ----------------
        summary_row = {
            "timestamp": ts,
            "frame_id": frame_id,
            "people_count": people_count,
            "violations_count": len(violations),
            "person_id": "",
            "missing": ""
        }
        storage.append_log(summary_row)

        # ---------------- Save EACH VIOLATION row ----------------
        for v in violations:
            v_row = {
                "timestamp": ts,
                "frame_id": frame_id,
                "people_count": people_count,
                "violations_count": len(violations),
                "person_id": v["person_id"],
                "missing": ",".join(v["missing"])
            }
            storage.append_log(v_row)

            # ---------------- EMAIL ALERT LOGIC ----------------
            if enable_email and smtp_user and smtp_password and recipients:
                for missing_item in v["missing"]:
                    vkey = f"{v['person_id']}_{missing_item}"

                    last_sent = st.session_state.last_email_times.get(vkey, 0)
                    current_ts = time.time()

                    if current_ts - last_sent >= email_cooldown:
                        subject = f"[SafetyEye] Violation: missing {missing_item}"
                        body = (
                            f"Time: {ts}\n"
                            f"Frame: {frame_id}\n"
                            f"Person ID: {v['person_id']}\n"
                            f"Missing PPE: {missing_item}\n\n"
                            f"Automated alert from SafetyEye Demo."
                        )

                        success = emailer.send_email_alert(
                            smtp_host=smtp_host,
                            smtp_port=int(smtp_port),
                            smtp_user=smtp_user,
                            smtp_password=smtp_password,
                            subject=subject,
                            body=body,
                            to_addrs=recipients,
                            use_ssl=int(smtp_port) == 465
                        )

                        if success:
                            st.session_state.last_email_times[vkey] = current_ts

        # ---------------- Display frame on UI ----------------
        feed_slot.image(frame_rgb, use_column_width=True)

        # Keep loop responsive
        time.sleep(0.5)

    # End of while — when stopped:
    if not st.session_state.running:
        st.info("Press START from the sidebar to run the simulator.")

# Allow page to work when run directly (Streamlit multipage top-left) or when imported by app.py
if __name__ == "__main__":
    app()
