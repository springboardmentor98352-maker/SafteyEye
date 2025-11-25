import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

def load_data():
    csv_path = Path("database/violations_log.csv")
    if not csv_path.exists():
        return pd.DataFrame(columns=["id","label","confidence","image","timestamp"])
    
    df = pd.read_csv(csv_path, header=None, names=["id","label","confidence","image","timestamp"])
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    return df


def app():

    st.subheader("📈 Analytics & Trends")

    df = load_data()

    if df.empty:
        st.info("⚠ No data available yet. Please run Live Monitor.")
        return

    # ===============================
    # KPI Cards
    # ===============================
    total = len(df)
    top_label = df["label"].value_counts().idxmax()
    avg_conf = df["confidence"].mean()

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='kpi-box'>📌 Total Logged<br><h2>{total}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-box'>🔥 Most Common<br><h2>{top_label}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-box'>🎯 Avg. Confidence<br><h2>{avg_conf:.2f}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ===============================
    # PIE CHART — Violation Type Distribution
    # ===============================
    st.subheader("🔍 Violation Breakdown")
    
    pie_fig = px.pie(
        df,
        names="label",
        title="Violation Type Distribution",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("---")

    # ===============================
    # TREND LINE — Violations Over Time
    # ===============================
    st.subheader("📆 Violation Trend Over Time")

    trend = df.groupby("date").size().reset_index(name="count")

    trend_fig = px.line(
        trend,
        x="date",
        y="count",
        markers=True,
        title="Violations vs Time",
        color_discrete_sequence=["cyan"]
    )

    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("---")

    # ===============================
    # TOP 5 VIOLATION BAR CHART
    # ===============================
    st.subheader("🏆 Top 5 Frequent Violations")

    top5 = df["label"].value_counts().head(5).reset_index()
    top5.columns = ["label", "count"]

    bar_fig = px.bar(
        top5,
        x="label",
        y="count",
        title="Most Logged Violations",
        color="label",
        color_discrete_sequence=px.colors.qualitative.Antique
    )

    st.plotly_chart(bar_fig, use_container_width=True)

    st.success("📊 Analytics updated successfully!")


