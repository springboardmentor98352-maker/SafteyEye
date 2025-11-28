import streamlit as st
import pandas as pd
import numpy as np

def app(state):
    st.subheader("👤 People Tracking")

    zones = state.get("zones", ["Assembly Line A", "Warehouse"])
    counts = np.random.randint(1, 80, size=len(zones))
    df = pd.DataFrame({"Zone": zones, "Current_Count": counts})
    st.table(df)

    st.markdown("---")
    st.subheader("Peak times (sample)")
    sample = pd.DataFrame({
        "Time Slot": ["8-10 AM", "10-12 PM", "12-2 PM", "2-4 PM", "4-6 PM"],
        "Avg_Occ": [65, 85, 45, 78, 52]
    }).set_index("Time Slot")
    st.bar_chart(sample, width="stretch")
