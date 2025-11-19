import streamlit as st
from utils.helpers import ensure_session_state


ensure_session_state()


def render_sidebar():
with st.sidebar:
st.image("assets/logo.png", use_container_width=True)
st.title("⚙️ Control Panel")


st.subheader("Monitoring Status")
if st.button("🟢 Start Monitoring" if not st.session_state.monitoring_active else "🔴 Stop Monitoring"):
st.session_state.monitoring_active = not st.session_state.monitoring_active


st.divider()


st.subheader("📍 Zone Selection")
st.session_state.zones = st.multiselect(
"Select zones to monitor:",
["Assembly Line A", "Assembly Line B", "Warehouse", "Loading Dock",
"Office Floor 1", "Office Floor 2", "Cafeteria", "Parking Area"],
default=["Assembly Line A", "Warehouse", "Loading Dock"]
)


st.divider()


st.subheader("🛡️ Safety Settings")
st.session_state.helmet_threshold = st.slider("Helmet Compliance %", 0, 100, 90)
st.session_state.vest_threshold = st.slider("Vest Compliance %", 0, 100, 85)
st.session_state.max_occupancy = st.number_input("Max Occupancy per Zone", 10, 200, 50)


st.divider()


st.subheader("🔔 Alert Settings")
st.session_state.alert_email = st.checkbox("Email Notifications", value=True)
st.session_state.alert_sound = st.checkbox("Sound Alerts", value=True)
st.session_state.alert_frequency = st.selectbox("Alert Frequency", ["Real-time", "Every 5 min", "Every 15 min"], index=0)


st.divider()


st.subheader("📊 Export Data")
if st.button("Download Report (PDF)"):
st.success("Report generated successfully!")
if st.button("Export Data (CSV)"):
st.success("Data exported successfully!")


st.markdown("---")
st.caption("Tip: Use the pages on the left to view Live Monitoring, Analytics, Alerts and People Tracking.")