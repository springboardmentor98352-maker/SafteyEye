import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def app(state):
    st.subheader("⚠️ Alerts & Notifications (mock)")

    times = pd.date_range(end=datetime.now(), periods=12, freq="15min")[::-1]
    df = pd.DataFrame({
        "Timestamp": times,
        "Zone": np.random.choice(state.get("zones", ["Assembly Line A"]), size=12),
        "Type": np.random.choice(["Helmet Violation", "Vest Violation", "Overcrowding"], size=12),
        "Severity": np.random.choice(["Critical", "Warning", "Info"], size=12),
        "Status": np.random.choice(["Resolved", "In Progress", "Pending"], size=12)
    })
    st.dataframe(df, width="stretch")
    st.markdown("**Tip:** Click a row to investigate (demo).")
