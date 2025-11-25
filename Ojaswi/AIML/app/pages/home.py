import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

def load_data():
    csv_path = Path("database/violations_log.csv")

    if not csv_path.exists():
        return pd.DataFrame(columns=["id","label","confidence","image","timestamp"])

    return pd.read_csv(csv_path, header=None, names=["id","label","confidence","image","timestamp"])


def app():
    st.subheader("📊 Dashboard Overview")

    df = load_data()

    # Metrics Section
    total = len(df)
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = len(df[df["timestamp"].astype(str).str.contains(today)]) if not df.empty else 0
    top_label = df["label"].value_counts().idxmax() if not df.empty else "None"
    avg_conf = df["confidence"].mean() if not df.empty else 0.0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Violations", total)
    col2.metric("Today's Violations", today_count)
    col3.metric("Most Common Violation", top_label)
    col4.metric("Avg Detection Confidence", f"{avg_conf:.2f}")

    st.write("---")

    st.subheader("🖼 Recent Violations")

    if df.empty:
        st.info("No records yet. Start Live Monitoring.")
        return

    recent = df.sort_values("timestamp", ascending=False).head(6)

    cols = st.columns(3)

    for i, row in recent.iterrows():
        block = cols[i % 3]
        block.markdown(f"**{row['label']} — {row['timestamp']}**")

        img_path = Path(row["image"])

        if img_path.exists():
            block.image(str(img_path), use_column_width=True)
        else:
            block.warning("Image Missing ⚠️")
