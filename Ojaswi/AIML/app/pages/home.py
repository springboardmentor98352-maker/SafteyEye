import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==========================================================
# LOAD DATA (ROBUST + OLD DATA SAFE)
# ==========================================================
def load_data():
    csv_path = Path("database/violations_log.csv")

    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])

    # 1️⃣ Read CSV safely even if some rows are broken
    df = pd.read_csv(
        csv_path,
        header=0,              # IMPORTANT: header exists in your file
        on_bad_lines="skip",   # skip corrupted rows (DOES NOT DELETE FILE)
        engine="python"
    )

    # 2️⃣ Force correct columns (old data compatible)
    expected_cols = ["id", "label", "confidence", "image", "timestamp"]
    df = df[[c for c in expected_cols if c in df.columns]]

    # 3️⃣ Fix confidence column (THIS FIXES YOUR ERROR)
    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")

    # 4️⃣ Drop rows where mandatory data is missing
    df = df.dropna(subset=["id", "label", "confidence", "image", "timestamp"])

    return df


# ==========================================================
# MAIN DASHBOARD PAGE
# ==========================================================
def app():
    st.subheader("📊 Dashboard Overview")

    df = load_data()

    # ===============================
    # METRICS (SAFE & FIXED)
    # ===============================
    total = len(df)

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = (
        df["timestamp"].astype(str).str.startswith(today_str).sum()
        if not df.empty else 0
    )

    top_label = df["label"].mode()[0] if not df.empty else "None"
    avg_conf = float(df["confidence"].mean()) if not df.empty else 0.0

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

        block.markdown(
            f"""
            <div style='padding:8px; font-weight:600'>
                {row['label']}<br>
                <span style='font-size:12px; color:gray'>{row['timestamp']}</span><br>
                <span style='font-size:12px'>Confidence: {float(row['confidence']):.2f}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        img_path = Path(row["image"])
        if img_path.exists():
            block.image(str(img_path), use_column_width=True)
        else:
            block.warning("⚠️ Image Missing")

