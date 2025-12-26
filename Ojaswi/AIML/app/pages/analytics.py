import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ------------------------------------------------
# LOAD VIOLATION LOGS
# ------------------------------------------------
def load_data():
    csv_path = Path("database/violations_log.csv")

    # Return empty DataFrame if CSV missing or empty
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])

    # Read CSV forcing column names (safe if CSV has no header)
    df = pd.read_csv(
        csv_path,
        header=None,
        names=["id", "label", "confidence", "image", "timestamp"]
    )

    # Convert confidence to numeric
    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")
    df = df.dropna(subset=["confidence"])

    # ---------------- Convert timestamp to datetime safely ----------------
    if "timestamp" in df.columns:
        df["timestamp"] = df["timestamp"].astype(str).str.strip()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["timestamp"])

        df["date"] = df["timestamp"].dt.date
        df["hour"] = df["timestamp"].dt.hour
    else:
        df["date"] = pd.NaT
        df["hour"] = pd.NaT

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
    # KPI STYLING
    # ------------------------------------------------
    st.markdown("""
    <style>
    .kpi-card-dark {
        background: #111827;
        padding: 18px;
        border-radius: 14px;
        text-align: center;
    }
    .kpi-title {
        color: #e5e7eb;
        font-size: 14px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

    # KPI CALCULATIONS
    total_violations = len(df)
    today = pd.Timestamp.today().date()
    today_count = len(df[df["date"] == today])
    avg_conf = df["confidence"].mean() if not df["confidence"].empty else 0
    most_common = df["label"].value_counts().idxmax() if not df["label"].empty else "N/A"

    col1, col2, col3, col4 = st.columns(4)

    for col, title, value in zip(
        [col1, col2, col3, col4],
        ["Total Violations", "Today's Violations", "Most Common Type", "Avg Confidence"],
        [total_violations, today_count, most_common, f"{avg_conf:.2f}"]
    ):
        col.markdown(f"""
        <div class="kpi-card-dark">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ------------------------------------------------
    # PIE CHART
    # ------------------------------------------------
    st.subheader("📌 Violation Type Distribution")
    fig_pie = px.pie(
        df,
        names="label",
        hole=0.45,
        color_discrete_sequence=["#1f2937", "#374151", "#4b5563", "#6b7280", "#9ca3af"]
    )
    fig_pie.update_layout(font_color="white")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------
    # TREND LINE
    # ------------------------------------------------
    st.subheader("📈 Violations Over Time")
    trend = df.groupby("date").size().reset_index(name="count")
    fig_line = px.line(
        trend,
        x="date",
        y="count",
        markers=True
    )
    fig_line.update_traces(marker=dict(color="#60a5fa", size=8))
    fig_line.update_layout(font_color="white")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------
    # TOP 5 VIOLATION TYPES
    # ------------------------------------------------
    st.subheader("🏆 Top 5 Violation Types")
    top5 = df["label"].value_counts().head(5).reset_index()
    top5.columns = ["label", "count"]
    fig_bar = px.bar(
        top5,
        x="label",
        y="count",
        color="label",
        color_discrete_sequence=["#60a5fa", "#3b82f6", "#1e40af", "#1e3a8a", "#172554"]
    )
    fig_bar.update_layout(font_color="white")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------
    # 🔥 VIOLATION HEATMAP (NEW FEATURE)
    # ------------------------------------------------
    st.subheader("🔥 Violation Heatmap (Date vs Hour)")
    heatmap_data = df.groupby(["date", "hour"]).size().reset_index(name="count")
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="hour",
        y="date",
        z="count",
        color_continuous_scale="inferno"
    )
    fig_heatmap.update_layout(
        font_color="white",
        xaxis_title="Hour of Day",
        yaxis_title="Date"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.success("📊 Analytics updated successfully with Violation Heatmap!")
