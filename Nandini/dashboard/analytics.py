import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def violation_pie_chart(logs):
    if len(logs) == 0:
        st.info("No violations yet to analyze.")
        return

    df = pd.DataFrame(logs)
    counts = df["Violation"].value_counts()

    fig, ax = plt.subplots(figsize=(3,3))
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
    st.pyplot(fig)

def alerts_panel(logs):
    st.subheader("🚨 Safety Alerts Panel")

    if len(logs) == 0:
        st.info("No alerts yet.")
        return

    # Filter options
    filter_choice = st.radio(
        "Filter Alerts By:",
        ["All", "Critical", "Warning"],
        horizontal=True
    )

    df = pd.DataFrame(logs)

    if filter_choice == "Critical":
        df = df[df["Severity"] == "Critical"]
    elif filter_choice == "Warning":
        df = df[df["Severity"] == "Warning"]

    if df.empty:
        st.success("No alerts under selected filter!")
        return

    # Display alerts
    for _, row in df.tail(10).iloc[::-1].iterrows():
        icon = "🔴" if row["Severity"] == "Critical" else "🟠"
        st.markdown(
            f"""
            <div style='padding:8px;margin-bottom:6px;border-left:6px solid {"#ff4d4d" if row["Severity"]=="Critical" else "#ff9800"};background:#fff5f5;border-radius:5px;'>
                {icon} <b>{row['Violation']}</b>  
                <br>
                <small>Worker: {row['Person']} | Time: {row['Time']}</small>
            </div>
            """,
            unsafe_allow_html=True)
        
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

