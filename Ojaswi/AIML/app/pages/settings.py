import streamlit as st
import json
from pathlib import Path

SETTINGS_FILE = Path("database/settings.json")



# ------------------------------
# Load Settings
# ------------------------------
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            return json.loads(SETTINGS_FILE.read_text())
        except:
            pass

    return {
        "confidence_threshold": 0.35,
        "audio_alerts": True,
        "generate_pdf": True,
        "sender": "",
        "receiver": "",
        "app_pass": ""
    }


# ------------------------------
# Save Settings
# ------------------------------
def save_settings(data):
    try:
        SETTINGS_FILE.write_text(json.dumps(data, indent=4))
        return True
    except:
        return False


# ------------------------------
# Streamlit Page
# ------------------------------
def app():

    st.subheader("⚙ Settings")
    st.caption("Update detection sensitivity, PDF, alerts & email configuration")

    settings = load_settings()

    # --------------------------
    # Detection Settings
    # --------------------------
    st.markdown("### 🎯 Detection Settings")

    confidence = st.slider(
        "Confidence Threshold",
        0.10, 1.00,
        settings.get("confidence_threshold", 0.35),
        step=0.01
    )

    audio_alerts = st.checkbox(
        "Enable Audio Alerts",
        settings.get("audio_alerts", True)
    )

    generate_pdf = st.checkbox(
        "Generate PDF Reports Automatically",
        settings.get("generate_pdf", True)
    )

    # --------------------------
    # Email Settings
    # --------------------------
    st.markdown("### 📧 Email Alert Configuration")

    sender = st.text_input("Sender Email (Gmail)", settings.get("sender", ""))
    receiver = st.text_input("Receiver Email", settings.get("receiver", ""))
    app_pass = st.text_input("App Password", settings.get("app_pass", ""), type="password")

    # --------------------------
    # Save Button
    # --------------------------
    if st.button("💾 Save Settings"):
        new_data = {
            "confidence_threshold": confidence,
            "audio_alerts": audio_alerts,
            "generate_pdf": generate_pdf,
            "sender": sender,
            "receiver": receiver,
            "app_pass": app_pass
        }

        if save_settings(new_data):
            st.success("✅ Settings Saved Successfully")
        else:
            st.error("❌ Failed to save settings")


    st.info("These settings affect Live Monitor & Email alerts.")