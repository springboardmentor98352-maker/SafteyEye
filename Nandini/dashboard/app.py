import streamlit as st
from simulation import generate_frame
from analytics import violation_pie_chart, alerts_panel
from report_generator import generate_pdf
from styles import load_css
import pandas as pd
import time
import random

# ---------------- WORKER DATABASE ----------------(fake)
if "worker_db" not in st.session_state:
    st.session_state.worker_db = pd.DataFrame({
        "Worker ID": [f"W{100+i}" for i in range(5)],
        "Name": ["Arjun", "Megha", "Ravi", "Sana", "Kiran"],
        "Zone": ["A", "B", "C", "A", "B"],
        "PPE Status": ["Safe", "Safe", "Safe", "Safe", "Safe"],
        "Last Seen": ["--"] * 5,
    })

# -----
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="SafetyEye Dashboard",
    layout="wide",
    page_icon="🛡"
)

# Load custom CSS
load_css()

# ----------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "logs" not in st.session_state:
    st.session_state.logs = []

if "today_count" not in st.session_state:
    st.session_state.today_count = 0

if "worker_count_history" not in st.session_state:
    st.session_state.worker_count_history = []

if "safe_history" not in st.session_state:
    st.session_state.safe_history = []

if "violation_history" not in st.session_state:
    st.session_state.violation_history = []



# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("🛡 SafetyEye – Real-Time Safety Monitoring")
st.write("AI-powered workplace safety monitoring & alert system.")

st.markdown("---")

# ----------------------------------------------------
# SIDEBAR CONTROLS
# ----------------------------------------------------
with st.sidebar:
    st.header("⚙️ Simulation Controls")

    show_boxes = st.checkbox("Show Human Figures", value=True)
    speed = st.slider("Speed (frames/sec)", 1, 10, 4)

    if st.button("▶ Start Simulation"):
        st.session_state.running = True

    if st.button("⏸ Stop Simulation"):
        st.session_state.running = False

    if st.button("🗑 Clear Logs"):
        st.session_state.logs = []
        st.session_state.today_count = 0

    st.markdown("---")

    st.subheader("📄 Report")
    if st.button("Generate PDF Report"):
        pdf_bytes = generate_pdf(
            total_alerts=len(st.session_state.logs),
            compliance=92  # placeholder
        )
        st.download_button(
            label="⬇ Download Report",
            data=pdf_bytes,
            file_name="safety_report.pdf",
            mime="application/pdf"
        )
        

# ----------------------------------------------------
# LIVE SIMULATION AREA
# ----------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("🎥 Live Safety Feed")

    placeholder = st.empty()

if st.session_state.running:
    for _ in range(50):

        before = len(st.session_state.logs)

        frame, worker_count = generate_frame(show_boxes)
        placeholder.image(frame, use_container_width=True)

        after = len(st.session_state.logs)
        frame_violations = max(0, after - before)

        # Track worker count
        st.session_state.worker_count_history.append(worker_count)

        # PPE trend
        safe = worker_count - frame_violations
        st.session_state.safe_history.append(safe)
        st.session_state.violation_history.append(frame_violations)

        # ------- WORKER TABLE UPDATE (THIS MUST BE HERE!) -------
        N = min(worker_count, len(st.session_state.worker_db))

        df = st.session_state.worker_db.copy()
        recent_logs = st.session_state.logs[-worker_count:] if worker_count > 0 else []

        for i in range(N):
            if i < len(recent_logs) and recent_logs[i]["Violation"] != "None":
                df.at[i, "PPE Status"] = recent_logs[i]["Violation"]
            else:
                df.at[i, "PPE Status"] = "Safe"

            df.at[i, "Last Seen"] = time.strftime("%H:%M:%S")

        st.session_state.worker_db = df
        # ----------------------------------------------------

        time.sleep(1 / speed)

        if not st.session_state.running:
            break

else:
    st.info("Click **Start Simulation** to begin.")



with right:
    st.subheader("📊 Safety Metrics")

    total_viol = len(st.session_state.logs)
    detected = 3  # simulated
    compliance = max(0, 100 - (total_viol * 2))

    m1, m2, m3 = st.columns(3)
    m1.metric("Detected", detected)
    m2.metric("Violations", total_viol)
    m3.metric("Compliance", f"{compliance}%")

    st.markdown("### 🚨 Alerts Summary")
    st.markdown(f"**Total Alerts Today:** {st.session_state.today_count}")

    alerts_panel(st.session_state.logs)

st.markdown("---")



# ----VIOLATION ANALYTICS SECTION-----
st.subheader("📈 Violation Analysis")
from analytics import worker_count_chart
from analytics import ppe_trend_chart

c1, c2 = st.columns(2)

with c1:
    violation_pie_chart(st.session_state.logs)

with c2:
    worker_count_chart(st.session_state.worker_count_history)

st.markdown("---")

c3, c4 = st.columns(2)

with c3:
    ppe_trend_chart(
        st.session_state.safe_history,
        st.session_state.violation_history
    )

with c4:
    st.info("More analytics can be added here (e.g., shift-wise performance).")
    
st.markdown("---")
st.subheader("📜 Violation Log")

if len(st.session_state.logs) > 0:
    df = pd.DataFrame(st.session_state.logs)
    st.dataframe(df.tail(20), use_container_width=True)
else:
    st.info("No violations recorded yet.")

st.markdown("---")
st.subheader("🧑‍🏭 Worker Identification Table")

df = st.session_state.worker_db.copy()

# Highlight unsafe workers
def highlight_status(row):
    color = "#ffcccc" if row["PPE Status"] != "Safe" else "#ccffcc"
    return [f'background-color: {color}'] * len(row)

st.dataframe(df.style.apply(highlight_status, axis=1), use_container_width=True)



# ----- ZONE SAFETY SECTION (STATIC FOR NOW)-----
st.markdown("---")
st.subheader("🗂 Zone Safety Overview")

zone_col1, zone_col2, zone_col3 = st.columns(3)

with zone_col1:
    st.markdown("""
    <div class='metric-card'>
        <h4>Zone A</h4>
        <p>Safety Score: <b>96%</b></p>
        <p>Alerts Today: <b>2</b></p>
    </div>
    """, unsafe_allow_html=True)

with zone_col2:
    st.markdown("""
    <div class='metric-card'>
        <h4>Zone B</h4>
        <p>Safety Score: <b>88%</b></p>
        <p>Alerts Today: <b>4</b></p>
    </div>
    """, unsafe_allow_html=True)

with zone_col3:
    st.markdown("""
    <div class='metric-card'>
        <h4>Zone C</h4>
        <p>Safety Score: <b>92%</b></p>
        <p>Alerts Today: <b>1</b></p>
    </div>
    """, unsafe_allow_html=True)
