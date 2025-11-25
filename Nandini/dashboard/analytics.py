import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import numpy as np

def violation_pie_chart(logs):
    st.subheader("📊 Violation Distribution")

    if len(logs) == 0:
        st.info("No violations yet to analyze.")
        return

    df = pd.DataFrame(logs)

    counts = df["Violation"].value_counts()

    # Different colors
    colors = {
        "Helmet Missing": "#ff4d4d",   # Red
        "No Vest": "#ff9800",          # Orange
        "No Boots": "#ffc107",         # Amber
        "Unsafe Posture": "#8e44ad",   # Purple
        "Zone Violation": "#2980b9",   # Blue
        "None": "#2ecc71"              # Green (Safe)
    }

    # Extract only violations (exclude "None")
    filtered_counts = counts.drop(labels=["None"], errors="ignore")

    if filtered_counts.empty:
        st.info("All detections are safe. No violations to show.")
        return

    #Colors for existing categories
    chart_colors = [colors.get(cat, "#999") for cat in filtered_counts.index]

    # Highlighting the largest violation
    explode = [0.1 if i == filtered_counts.idxmax() else 0 
               for i in filtered_counts.index]

    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    ax.pie(
        filtered_counts,
        labels=[f"{cat} ({count})" for cat, count in filtered_counts.items()],
        autopct="%1.1f%%",
        explode=explode,
        colors=chart_colors,
        shadow=True,
        startangle=140,
        textprops={'fontsize': 9}
    )

    ax.set_title("Violation Breakdown", fontsize=13)
    st.pyplot(fig)


VIOLATION_ICONS = {
    "Helmet Missing": "🪖",
    "No Vest": "🦺",
    "No Boots": "👢",
    "Unsafe Posture": "⚠️",
    "Zone Violation": "🚫",
    "None": "✔️"
}

SEVERITY_COLORS = {
    "Critical": "#ff4d4d",
    "Warning": "#ff9800",
    "Safe": "#4CAF50"
}


def alerts_panel(logs):
    st.subheader("🚨 Smart Alerts Panel")

    if len(logs) == 0:
        st.info("No alerts yet.")
        return

    df = pd.DataFrame(logs)

    # --- FILTER OPTIONS ---
    filter_choice = st.radio(
        "Filter Alerts By:",
        ["All", "Critical", "Warning", "Repeated Violators"],
        horizontal=True
    )

    if filter_choice == "Critical":
        df = df[df["Severity"] == "Critical"]
    elif filter_choice == "Warning":
        df = df[df["Severity"] == "Warning"]
    elif filter_choice == "Repeated Violators":
        viol_counts = df["Person"].value_counts()
        frequent = viol_counts[viol_counts >= 3].index
        df = df[df["Person"].isin(frequent)]

    if df.empty:
        st.success("No alerts under selected filter!")
        return

    # Show newest alerts first
    df = df.iloc[::-1].head(15)

    # --- ALERT CARDS ---
    for _, row in df.iterrows():
        vio = row["Violation"]
        sev = row["Severity"]
        icon = VIOLATION_ICONS.get(vio, "⚠️")
        border_color = SEVERITY_COLORS.get(sev, "#999")

        glow = "box-shadow: 0 0 12px rgba(255,0,0,0.6);" if sev == "Critical" else ""

        st.markdown(
            f"""
            <div style="
                padding:10px;
                margin-bottom:8px;
                border-left:6px solid {border_color};
                border-radius:8px;
                background:#fff5f5;
                {glow}
            ">
                <b>{icon} {vio}</b> 
                <br>
                <small>
                    👷 Worker: <b>{row['Person']}</b> 
                    &nbsp;|&nbsp;
                    🕒 Time: {row['Time']} 
                    &nbsp;|&nbsp;
                    🔥 Severity: 
                    <span style="color:{border_color};font-weight:bold;">{sev}</span>
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---- CLOSE SCROLL BOX DIV ----
st.markdown("</div>", unsafe_allow_html=True)
        
def worker_count_chart(counts):
    if len(counts) < 2:
        st.info("Not enough data yet to plot worker count.")
        return

    st.subheader("👷‍♂️ Worker Count Over Time")

    fig, ax = plt.subplots()
    ax.plot(counts, marker='o', linewidth=2)
    ax.set_ylim(0, 6)  
    ax.set_xlabel("Frame")
    ax.set_ylabel("Workers Detected")
    ax.set_title("Worker Count Trend")
    st.pyplot(fig)

def ppe_trend_chart(safe_list, viol_list):
    if len(safe_list) < 2:
        st.info("Not enough data yet for PPE trend chart.")
        return

    st.subheader("📉 PPE Compliance Trend")

    frames = list(range(1, len(safe_list) + 1))

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(frames, safe_list, marker='o', color='green', label='Safe Detections')
    ax.plot(frames, viol_list, marker='o', color='red', label='Violations')

    ax.set_xlabel("Frame")
    ax.set_ylabel("Count")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

def get_shift(time_string):
    """Return shift name based on HH:MM:SS time."""
    t = datetime.datetime.strptime(time_string, "%H:%M:%S").time()

    if datetime.time(6, 0) <= t < datetime.time(14, 0):
        return "Morning"
    elif datetime.time(14, 0) <= t < datetime.time(22, 0):
        return "Afternoon"
    else:
        return "Night"
    

def shift_summary(logs):
    if len(logs) == 0:
        st.info("No data yet for shift analysis.")
        return
    
    df = pd.DataFrame(logs)
    df["Shift"] = df["Time"].apply(get_shift)

    # Total detections per shift
    shift_totals = df["Shift"].value_counts()

    # Violations per shift (non-"None")
    shift_viol = df[df["Violation"] != "None"]["Shift"].value_counts()

    # Build summary
    st.subheader("⏱️ Shift-wise Safety Summary")

    for shift in ["Morning", "Afternoon", "Night"]:
        total = shift_totals.get(shift, 0)
        viol = shift_viol.get(shift, 0)

        if total == 0:
            compliance = "No data"
        else:
            compliance = f"{max(0, 100 - int((viol/total)*100))}%"

        st.markdown(
            f"""
            <div style='padding:10px;margin:5px;border-radius:8px;border-left:5px solid #4c8bf5;background:#f5f8ff;'>
                <b>{shift} Shift</b><br>
                Compliance: <b>{compliance}</b><br>
                Violations: <b>{viol}</b> / Total Events: {total}
            </div>
            """,
            unsafe_allow_html=True
        )

def alert_frequency_radar(logs):
    st.subheader("📡 Alert Frequency Radar Chart")

    if len(logs) == 0:
        st.info("No alerts yet to visualize.")
        return

    df = pd.DataFrame(logs)

    # Define alert categories (future-proof)
    categories = [
        "Helmet Missing",
        "No Vest",
        "No Boots",
        "Unsafe Posture",
        "Zone Violation"
    ]

    # Count occurrences
    values = [df["Violation"].value_counts().get(cat, 0) for cat in categories]

    # Radar chart requires closing the circle
    values += values[:1]  
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # Creating the radar plot
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title("Alert Frequency Radar", pad=20)

    st.pyplot(fig)

