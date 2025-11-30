import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ------------------------------------------------
# LOAD VIOLATION LOGS
# ------------------------------------------------
def load_data():
    csv_path = Path("database/violations_log.csv")

    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])

    df = pd.read_csv(csv_path, header=None, names=["id", "label", "confidence", "image", "timestamp"])
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    return df


# ------------------------------------------------
# MAIN PAGE
# ------------------------------------------------
def app():

    st.subheader("📊 Analytics & Violation Insights")

    df = load_data()

    if df.empty:
        st.info("⚠ No data available yet. Please run Live Monitoring.")
        return

    # ------------------------------------------------
    # KPI STYLING (MAKE TEXT WHITE)
    # ------------------------------------------------
    st.markdown("""
    <style>
    .kpi-title { color: #e5e7eb !important; }
    .kpi-value { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

    # KPI CALCULATIONS
    total_violations = len(df)
    today = pd.Timestamp.today().date()
    today_count = len(df[df["date"] == today])
    avg_conf = df["confidence"].mean()
    most_common = df["label"].value_counts().idxmax()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card-dark">
                <div class="kpi-title">Total Violations</div>
                <div class="kpi-value">{total_violations}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card-dark">
                <div class="kpi-title">Today's Violations</div>
                <div class="kpi-value">{today_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card-dark">
                <div class="kpi-title">Most Common Type</div>
                <div class="kpi-value">{most_common}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card-dark">
                <div class="kpi-title">Avg Confidence</div>
                <div class="kpi-value">{avg_conf:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------------------------------------
    # PIE CHART — Dark Theme Colors
    # ------------------------------------------------
    st.subheader("📌 Violation Type Distribution")

    dark_palette = ["#1f2937", "#374151", "#4b5563", "#6b7280", "#9ca3af"]

    fig_pie = px.pie(
        df,
        names="label",
        title="Violation Breakdown",
        hole=0.45,
        color_discrete_sequence=dark_palette
    )

    fig_pie.update_layout(
        title_font_color="white",
        legend_font_color="white",
        font_color="white"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------
    # TREND LINE — White Line on Dark Background
    # ------------------------------------------------
    st.subheader("📈 Violations Over Time")

    trend = df.groupby("date").size().reset_index(name="count")

    fig_line = px.line(
        trend,
        x="date",
        y="count",
        markers=True,
        title="Daily Violation Trend",
        color_discrete_sequence=["white"]
    )

    fig_line.update_traces(marker=dict(color="#60a5fa", size=8))  # blue markers

    fig_line.update_layout(
        title_font_color="white",
        font_color="white",
        xaxis_title=None,
        yaxis_title=None
    )

    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------
    # TOP 5 VIOLATION TYPES — Dark Blue Bars
    # ------------------------------------------------
    st.subheader("🏆 Top 5 Violation Types")

    top5 = df["label"].value_counts().head(5).reset_index()
    top5.columns = ["label", "count"]

    fig_bar = px.bar(
        top5,
        x="label",
        y="count",
        title="Most Frequent Violations",
        color="label",
        color_discrete_sequence=["#60a5fa", "#3b82f6", "#1e40af", "#1e3a8a", "#172554"]
    )

    fig_bar.update_layout(
        title_font_color="white",
        legend_font_color="white",
        font_color="white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.success("📊 Analytics updated successfully!")

