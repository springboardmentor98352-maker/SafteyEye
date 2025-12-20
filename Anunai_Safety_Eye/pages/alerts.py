"""
pages/alerts.py

Alerts / Incidents page for SafetyEye Dashboard.

Features:
- Reads logs from core.storage.read_logs()
- Shows recent logs (latest 500)
- Date range filter and text search (person_id, missing)
- Clear stored logs button (deletes logs.csv via storage.clear_logs if present)
- Export logs to CSV
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from core import storage

# Optional: path to internship PDF (your local copy). Update if you want a clickable reference.
PROJECT_PDF_PATH = r"C:\Users\anuna\OneDrive\Desktop\Anunai code\virtual_intern\Saftey_Eye.pdf"

def safe_clear_logs():
    """
    Try to clear logs using storage.clear_logs() if available.
    Otherwise attempt to remove the CSV file used by storage.
    """
    if hasattr(storage, "clear_logs") and callable(storage.clear_logs):
        storage.clear_logs()
        return True
    # fallback: try to remove storage CSV_PATH if exposed
    csv_path = getattr(storage, "CSV_PATH", None)
    if csv_path and os.path.exists(csv_path):
        try:
            os.remove(csv_path)
            return True
        except Exception as e:
            print("Failed to delete CSV in fallback clear:", e)
            return False
    # last fallback: attempt to remove ../logs.csv relative to this file
    fallback = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs.csv")
    if os.path.exists(fallback):
        try:
            os.remove(fallback)
            return True
        except Exception as e:
            print("Failed to delete fallback logs.csv:", e)
            return False
    return False

def app():
    st.title("Alerts / Incidents")
    st.markdown("This page shows violations and frame summaries recorded by the Live Monitor.")
    st.caption(f"Project brief (local): {PROJECT_PDF_PATH}")

    # Read logs
    rows = storage.read_logs(limit=20000)
    if not rows:
        st.info("No logs recorded yet. Start the monitor to generate demo data.")
        return

    # Build DataFrame
    df = pd.DataFrame(rows)

    # Normalize columns and types (safe conversions)
    for col in ["people_count", "violations_count"]:
        if col not in df.columns:
            df[col] = 0
    if "person_id" not in df.columns:
        df["person_id"] = ""
    if "missing" not in df.columns:
        df["missing"] = ""

    df["people_count"] = pd.to_numeric(df["people_count"], errors="coerce").fillna(0).astype(int)
    df["violations_count"] = pd.to_numeric(df["violations_count"], errors="coerce").fillna(0).astype(int)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Top controls: quick filters
    st.subheader("Filters")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        # default range: last 24 hours
        max_time = df["timestamp"].max()
        min_time = df["timestamp"].min()
        if pd.isna(max_time):
            max_time = pd.Timestamp.now()
        if pd.isna(min_time):
            min_time = max_time - pd.Timedelta(days=1)
        start_dt = st.date_input("Start date", value=min_time.date(), key="alerts_start")
    with col2:
        end_dt = st.date_input("End date", value=max_time.date(), key="alerts_end")
    with col3:
        search_text = st.text_input("Search (person_id or violation text)", value="", placeholder="e.g. person_2, helmet")

    # Convert date inputs to timestamps for filtering (include full days)
    start_ts = pd.to_datetime(start_dt)
    end_ts = pd.to_datetime(end_dt) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    # Apply filters
    filtered = df[
        (df["timestamp"] >= start_ts) &
        (df["timestamp"] <= end_ts)
    ].copy()

    if search_text.strip():
        st.caption(f"Filtering rows containing: '{search_text}'")
        mask = (
            filtered["person_id"].astype(str).str.contains(search_text, case=False, na=False) |
            filtered["missing"].astype(str).str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    # Show summary metrics at top of page
    st.markdown("---")
    st.subheader("Summary")
    total_rows = len(filtered)
    total_violations = filtered[filtered["person_id"].astype(str).str.strip() != ""].shape[0]
    total_people = filtered["people_count"].sum()
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Rows (filtered)", total_rows)
    col_b.metric("Violations (filtered)", total_violations)
    col_c.metric("People (frames filtered)", total_people)

    # Recent logs table (latest 500 rows)
    st.subheader("Recent logs (latest 500 rows)")
    display_df = filtered.sort_values("timestamp", ascending=False).head(500)
    # For better display, fill NaNs with empty strings
    display_df = display_df.fillna("")
    st.dataframe(display_df)

    # Manage logs: Clear button (dangerous)
    st.markdown("---")
    st.subheader("Manage Logs")
    st.write("⚠️ Clearing logs will permanently delete stored logs (CSV). This cannot be undone.")
    if st.button("Clear stored logs (DELETES CSV)"):
        ok = safe_clear_logs()
        st.session_state.logs = []
        if ok:
            st.success("Logs cleared from storage.")
        else:
            st.error("Failed to clear logs. Check file permissions or storage implementation.")
        st.rerun()

    # Export
    st.markdown("---")
    st.subheader("Export")
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered logs CSV", data=csv, file_name="safeteye_logs_filtered.csv", mime="text/csv")

    # Also offer full export
    st.markdown("#### Full export")
    csv_all = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download ALL logs CSV", data=csv_all, file_name="safeteye_logs_all.csv", mime="text/csv")

    st.markdown("---")
    st.caption("Tip: Use the Live Monitor to generate demo logs, then come here to inspect, filter and export incidents.")

if __name__ == "__main__":
    app()
