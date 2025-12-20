import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime


# ==========================================================
# LOAD DATA SAFELY
# ==========================================================
def load_data():
    csv_path = Path("database/violations_log.csv")

    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])

    try:
        df = pd.read_csv(csv_path, header=None, names=["id", "label", "confidence", "image", "timestamp"])
        return df
    except:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])


# ==========================================================
# MAIN DASHBOARD PAGE
# ==========================================================
def app():

    st.subheader("📊 Dashboard Overview")

    df = load_data()

    # ===============================
    # METRICS (SAFE)
    # ===============================
    total = len(df)

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = df["timestamp"].astype(str).str.startswith(today_str).sum() if not df.empty else 0

    top_label = df["label"].mode()[0] if not df.empty else "None"

    avg_conf = df["confidence"].mean() if not df.empty else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Violations", total)
    col2.metric("Today's Violations", today_count)
    col3.metric("Most Common Violation", top_label)
    col4.metric("Avg Confidence", f"{avg_conf:.2f}")

    st.markdown("---")

    # ===============================
    # RECENT VIOLATIONS
    # ===============================
    st.subheader("🖼 Recent Violations")

    if df.empty:
        st.info("No violation logs yet. Start Live Monitoring.")
        return

    recent = df.sort_values("timestamp", ascending=False).head(6)

    cols = st.columns(3)

    for i, row in recent.iterrows():
        block = cols[i % 3]

        timestamp = row["timestamp"]
        label = row["label"]
        img_path = Path(row["image"])

        block.markdown(f"""
        <div style='padding:8px; font-weight:600'>
            {label}<br>
            <span style='font-size:12px; color:gray'>{timestamp}</span>
        </div>
        """, unsafe_allow_html=True)

        if img_path.exists():
            block.image(str(img_path), use_column_width=True)
        else:
            block.warning("⚠️ Image Missing")
