import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd
import time
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="SafetyEye Dashboard", layout="wide")


# ==== HEADER ====
st.markdown("""
    <h1 style='font-family:Arial; color:#004AAD;'>🟦 SafetyEye – Real-Time Workplace Safety Dashboard</h1>
    <p style='font-size:16px; color:#333;'>AI-powered PPE monitoring • Incident analytics • Compliance insights</p>
""", unsafe_allow_html=True)


# ==== SESSION STATE ====
if "running" not in st.session_state:
    st.session_state.running = False

if "logs" not in st.session_state:
    st.session_state.logs = []

if "today_count" not in st.session_state:
    st.session_state.today_count = 0


# =====SIDEBAR =====
with st.sidebar:
    st.markdown("<h2 style='color:#004AAD;'>⚙️ Controls</h2>", unsafe_allow_html=True)
    
    show_boxes = st.checkbox("Show Body Overlays", value=True)
    speed = st.slider("Speed (frames/sec)", 1, 10, 4)

    if st.button("▶ Start Simulation"):
        st.session_state.running = True

    if st.button("⏸ Stop Simulation"):
        st.session_state.running = False

    if st.button("🗑 Clear Logs"):
        st.session_state.logs = []
        st.session_state.today_count = 0


# ==== HUMAN FIGURE ====
def draw_human(draw, x, y, color):
    draw.ellipse([x+20, y, x+40, y+20], fill=color)
    draw.rectangle([x+25, y+20, x+35, y+60], fill=color)
    draw.line([(x+25, y+30), (x, y+45)], fill=color, width=4)
    draw.line([(x+35, y+30), (x+60, y+45)], fill=color, width=4)
    draw.line([(x+27, y+60), (x+10, y+100)], fill=color, width=4)
    draw.line([(x+33, y+60), (x+50, y+100)], fill=color, width=4)


# ==== FRAME GENERATION ====
def generate_frame(show_boxes=True):
    img = Image.new("RGB", (700, 450), "white")
    draw = ImageDraw.Draw(img)

    for i in range(5):
        x = np.random.randint(50, 500)
        y = np.random.randint(80, 250)

        violation = np.random.choice(
            ["None", "Helmet Missing", "No Vest", "No Boots"],
            p=[0.55, 0.25, 0.12, 0.08]
        )

        severity = ("Critical" if violation == "Helmet Missing"
                    else "Warning" if violation != "None"
                    else "Safe")

        color = "green" if violation == "None" else "red"

        if show_boxes:
            draw_human(draw, x, y, color)
            draw.text((x, y - 10), f"P{i+1}: {severity}", fill=color)

        if violation != "None":
            st.session_state.logs.append({
                "Time": time.strftime("%H:%M:%S"),
                "Person": f"P{i+1}",
                "Violation": violation,
                "Severity": severity
            })
            st.session_state.today_count += 1

    return img


# ==== LAYOUT: LIVE FEED + METRICS ====
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎥 Live Safety Feed")
    placeholder = st.empty()

    if st.session_state.running:
        for _ in range(60):
            frame = generate_frame(show_boxes)
            placeholder.image(frame, use_container_width=True)
            time.sleep(1 / speed)
            if not st.session_state.running:
                break
    else:
        st.info("Click **Start Simulation** to begin.")


with col2:
    st.subheader("📊 Key Safety Metrics")

    total_violations = len(st.session_state.logs)
    compliance = max(1, 100 - total_violations)

    card_style = "padding:15px; border-radius:10px; background-color:#e8f1ff; color:#004AAD;"

    st.markdown(f"<div style='{card_style}'><h3>{st.session_state.today_count}</h3>Today's Alerts</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{card_style}'><h3>{compliance}%</h3>Compliance Rate</div>", unsafe_allow_html=True)


    st.subheader("🟠 PPE Breakdown")
    if total_violations > 0:
        df = pd.DataFrame(st.session_state.logs)
        counts = df["Violation"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(3,3))
        ax2.pie(counts, labels=counts.index, autopct='%1.1f%%')
        st.pyplot(fig2)
    else:
        st.info("No violations yet.")


    st.subheader("🚨 Alerts Feed")
    if len(st.session_state.logs) > 0:
        for row in st.session_state.logs[-5:][::-1]:
            icon = "🔴" if row["Severity"] == "Critical" else "🟠"
            st.write(f"{icon} **{row['Violation']}** – {row['Time']} (P{row['Person'][-1]})")
    else:
        st.info("No active alerts.")


# ==== INSIGHTS ====
st.markdown("---")
st.subheader("📌 Insights Summary")

st.info("""
- Helmet Missing is the top PPE violation today.  
- Alerts peak around 2 PM – 4 PM.  
- Safety compliance has improved since yesterday.  
- Zone B tends to have more PPE non-compliance events.
""")


# ==== ZONE SAFETY ====
st.subheader("🗺️ Zone Risk Levels")

z1, z2, z3 = st.columns(3)
z1.metric("Zone A", "82%", "Safe")
z2.metric("Zone B", "68%", "Moderate Risk")
z3.metric("Zone C", "91%", "Safe")


# ==== VIOLATION LOG TABLE ====
st.subheader("📜 Full Violation Log")

if len(st.session_state.logs) > 0:
    st.dataframe(pd.DataFrame(st.session_state.logs), use_container_width=True)
else:
    st.info("No violation records yet.")


# ============================= PDF REPORT GENERATION =============================
st.markdown("---")
st.subheader("📄 Generate Safety Report")

def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(50, 750, "SafetyEye – Daily Safety Report")
    c.drawString(50, 720, f"Total Alerts: {st.session_state.today_count}")
    c.drawString(50, 700, f"Compliance: {compliance}%")

    c.drawString(50, 660, "Insights:")
    c.drawString(70, 640, "- Helmet Missing is the top violation.")
    c.drawString(70, 620, "- Alerts peak during afternoon hours.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

if st.button("📄 Download PDF Report"):
    pdf = generate_pdf()
    st.download_button("Click to download", pdf, file_name="safety_report.pdf")

