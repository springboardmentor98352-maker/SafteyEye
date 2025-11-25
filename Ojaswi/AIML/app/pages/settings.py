import streamlit as st
import json
from pathlib import Path
import os

SETTINGS_FILE = Path("database/settings.json")


# -------------------------
# Load & Save Settings
# -------------------------

def load_settings():
    if not SETTINGS_FILE.exists():
        return {
            "confidence_threshold": 0.35,
            "audio_alerts": True,
            "generate_pdf": True
        }
    return json.loads(SETTINGS_FILE.read_text())


def save_settings(settings):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4))


# -------------------------
# Clear Data Helper
# -------------------------

def clear_all_data():
    db_folder = Path("database")
    for file in db_folder.glob("*"):
        if file.name != "settings.json":  # don't delete settings
            file.unlink()


# -------------------------
# MAIN PAGE UI
# -------------------------
def app():
    st.subheader("⚙️ Application Settings")

    settings = load_settings()

    # ---- UI Controls ----
    st.markdown("### 🔧 Detection Preferences")

    # Confidence Setting
    new_conf = st.slider(
        "Minimum Detection Confidence",
        min_value=0.2,
        max_value=1.0,
        step=0.05,
        value=settings["confidence_threshold"]
    )

    # Toggle Controls
    audio = st.checkbox("Enable Audio Alerts 🔊", value=settings["audio_alerts"])
    make_pdf = st.checkbox("Auto-Generate Violation PDF 📄", value=settings["generate_pdf"])

    # Save Button
    if st.button("💾 Save Settings"):
        settings["confidence_threshold"] = new_conf
        settings["audio_alerts"] = audio
        settings["generate_pdf"] = make_pdf
        save_settings(settings)
        st.success("✅ Settings Updated")

    st.markdown("---")
    st.subheader("🧹 Maintenance Tools")

    # ---- CLEAR DATABASE ----
    if st.button("🗑 Clear All Violation Records"):
        clear_all_data()
        st.warning("⚠️ All violation images, logs & PDFs deleted!")

    # Reset system
    if st.button("🔄 Reset System to Default"):
        SETTINGS_FILE.unlink(missing_ok=True)
        st.success("System Reset — Restart App to Apply Changes.")


    st.markdown("---")
    st.info("💡 Settings are stored permanently and will apply across all sessions.")
