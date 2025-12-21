import streamlit as st
import cv2
import pandas as pd
import random
import time

# ---------------- CONFIG ----------------
st.set_page_config("SafetyEye – AI Safety Dashboard", layout="wide")

# ---------------- STATE ----------------
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "camera" not in st.session_state:
    st.session_state.camera = False
if "people" not in st.session_state:
    st.session_state.people = []

ZONES = ["Assembly Line A", "Assembly Line B", "Warehouse", "Loading Dock"]

# ---------------- MOCK PEOPLE (10+) ----------------
def generate_people():
    data = []
    for i in range(1, 11):
        data.append({
            "Person ID": f"P{i:02d}",
            "Zone": random.choice(ZONES),
            "Helmet": random.choice([True, True, False]),
            "Vest": random.choice([True, True, False]),
            "Time": time.strftime("%H:%M:%S")
        })
    return data

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛡 SafetyEye\nControl Panel")

st.session_state.monitoring = st.sidebar.toggle("Start Monitoring")
st.session_state.camera = st.sidebar.toggle("📷 Camera Access")

selected_zones = st.sidebar.multiselect(
    "Select Zones",
    ZONES,
    default=["Assembly Line A"]
)

helmet_limit = st.sidebar.slider("Helmet Compliance %", 50, 100, 85)
vest_limit = st.sidebar.slider("Vest Compliance %", 50, 100, 85)
max_occ = st.sidebar.slider("Max Occupancy per Zone", 5, 50, 10)

sound_alert = st.sidebar.checkbox("🔊 Sound Alerts", True)
email_alert = st.sidebar.checkbox("📧 Email Alerts", True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🛡 SafetyEye – AI Safety Dashboard</h1>", unsafe_allow_html=True)
tabs = st.tabs(["🔴 Live Monitoring", "📊 Analytics", "⚠ Alerts", "👥 People Tracking"])

# ==================================================
# LIVE MONITORING
# ==================================================
with tabs[0]:
    st.subheader("🔴 Live Monitoring")

    if st.session_state.monitoring:
        st.session_state.people = generate_people()
    else:
        st.info("Turn ON monitoring to generate data")

    df = pd.DataFrame(st.session_state.people)

    # ✅ APPLY ZONE FILTER (FIX)
    df = df[df["Zone"].isin(selected_zones)]

    total = len(df)

    helmet_pct = int((df["Helmet"].sum() / total) * 100) if total else 0
    vest_pct = int((df["Vest"].sum() / total) * 100) if total else 0

    violations = len(
        df[(df["Helmet"] == False) | (df["Vest"] == False)]
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Occupancy", total)
    c2.metric("Avg Helmet %", helmet_pct)
    c3.metric("Avg Vest %", vest_pct)
    c4.metric("Violations", violations)

    st.markdown("### 👥 Live Detected People")

    if total:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No people in selected zones")

    # ---------------- CAMERA ----------------
    if st.session_state.monitoring and st.session_state.camera:
        st.subheader("📷 Live Camera Feed")
        cap = cv2.VideoCapture(0)
        frame_box = st.empty()
        alert_box = st.empty()

        for _ in range(40):
            ret, frame = cap.read()
            if not ret:
                break

            helmet = random.choice([True, False, True])

            if not helmet:
                alert_box.warning("⚠ Helmet NOT detected! Please wear helmet.")
            else:
                alert_box.success("✅ Helmet detected")

            cv2.putText(
                frame,
                f"Helmet: {'YES' if helmet else 'NO'}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0) if helmet else (0,0,255),
                2
            )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_box.image(frame)
            time.sleep(0.1)

        cap.release()

    else:
        st.info("Enable monitoring and camera to view feed")

# ==================================================
# ANALYTICS
# ==================================================
with tabs[1]:
    st.subheader("📊 Analytics")

    if total:
        st.bar_chart(df["Zone"].value_counts())
    else:
        st.info("No analytics data")

# ==================================================
# ALERTS
# ==================================================
with tabs[2]:
    st.subheader("⚠ Alerts")

    if violations == 0:
        st.success("No violations 🎉")
    else:
        st.error(f"{violations} safety violations detected")

        if sound_alert:
            st.warning("🔊 Sound alert triggered")
        if email_alert:
            st.info("📧 Email alert sent")

# ==================================================
# PEOPLE TRACKING
# ==================================================
with tabs[3]:
    st.subheader("👥 People Tracking")

    if total:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No people to track")

# ---------------- FOOTER ----------------
st.markdown("<hr><center>© SafetyEye | AI Workplace Safety System</center>", unsafe_allow_html=True)
