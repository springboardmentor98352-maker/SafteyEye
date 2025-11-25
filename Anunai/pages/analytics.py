"""
pages/analytics.py

Analytics:
- Violations over time (hourly)
- Compliance rate (pie or stacked)
- Top violation types (bar)
"""

import streamlit as st
from core import storage
import pandas as pd
import plotly.express as px

def app():
    st.title("Analytics")
    rows = storage.read_logs(limit=20000)
    if not rows:
        st.info("No logs yet. Run Live Monitor to create demo data.")
        return

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["people_count"] = pd.to_numeric(df["people_count"], errors="coerce").fillna(0).astype(int)
    df["violations_count"] = pd.to_numeric(df["violations_count"], errors="coerce").fillna(0).astype(int)
    df["person_id"] = df["person_id"].astype(str)
    df["missing"] = df["missing"].astype(str)

    # --- Violations over time (hourly) ---
    # Count violation rows: we consider a "violation row" any row where person_id is not empty
    violation_rows = df[df["person_id"].str.strip() != ""].copy()
    if violation_rows.empty:
        st.info("No recorded violations yet.")
    else:
        viol_by_hour = violation_rows.set_index("timestamp").resample("H").size().reset_index(name="violations")
        fig1 = px.line(viol_by_hour, x="timestamp", y="violations", title="Violations over time (hourly)")
        st.plotly_chart(fig1, use_container_width=True)

    # --- Compliance rate ---
    # Use frame summary rows (person_id empty) to compute people seen per frame
    frame_summaries = df[df["person_id"].str.strip() == ""].copy()
    total_people = frame_summaries["people_count"].sum()
    total_violations = len(violation_rows)
    compliance_rate = 0.0
    if total_people > 0:
        # compliance is 1 - (total_violations / total_people)
        compliance_rate = max(0.0, 1.0 - (total_violations / total_people))
    st.subheader("Compliance")
    st.metric("Compliance rate", f"{compliance_rate*100:.2f}%")
    # show pie: compliant vs non-compliant counts (approx)
    compliant_count = max(0, total_people - total_violations)
    non_compliant_count = total_violations
    comp_df = pd.DataFrame({
        "status": ["compliant", "non_compliant"],
        "count": [compliant_count, non_compliant_count]
    })
    fig_comp = px.pie(comp_df, names="status", values="count", title="Compliance distribution")
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- Top violation types ---
    if not violation_rows.empty:
        # violation types are in 'missing' column (comma sep). Use get_dummies trick.
        dummies = violation_rows["missing"].str.get_dummies(sep=",")
        if dummies.shape[1] == 0:
            st.write("No violation types found in logs.")
        else:
            types = dummies.sum().reset_index()
            types.columns = ["violation", "count"]
            types_sorted = types.sort_values("count", ascending=False)
            fig_bar = px.bar(types_sorted, x="violation", y="count", title="Top violation types")
            st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")
    st.caption("Note: These analytics are computed from demo logs. When integrated with a real model, logs will reflect real detections.")

if __name__ == "__main__":
    app()
