import streamlit as st
import pandas as pd
from data import mock_data
from components import widgets

def app(state):
    st.subheader("🎥 Live Monitoring — Overview")

    zones = state.get("zones", ["Assembly Line A"])
    max_cap = state.get("max_capacity", 50)
    data = mock_data.gen_occupancy(zones, max_cap)
    df = pd.DataFrame(data)
    df["utilization"] = (df["current"] / df["max_capacity"] * 100).round(1)
    df["overall_compliance"] = ((df["helmet_compliance"] + df["vest_compliance"]) / 2).round(1)

    # KPI row
    total = int(df["current"].sum())
    avg_helmet = int(df["helmet_compliance"].mean())
    avg_vest = int(df["vest_compliance"].mean())

    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.markdown("<div class='card'><div class='kpi'>👥 "+str(total)+"</div><div class='kpi-sub'>Total people now</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><div class='kpi'>🪖 {avg_helmet}%</div><div class='kpi-sub'>Avg Helmet Compliance</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><div class='kpi'>🦺 {avg_vest}%</div><div class='kpi-sub'>Avg Vest Compliance</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Zone Details")
    # use width='stretch' per deprecation notice
    st.dataframe(df, width="stretch")

    st.markdown("---")
    st.subheader("Camera Feed Mockups")
    # show placeholders for the selected zones in grid
    cols = st.columns(min(3, len(zones)))
    for i, zone in enumerate(zones):
        col = cols[i % len(cols)]
        with col:
            st.markdown(f"**📹 {zone}**")
            # small placeholder image via datauri or styled box
            st.markdown(f"<div style='background:#08101a;height:120px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#7fb5e6;'>Camera feed placeholder</div>", unsafe_allow_html=True)
            st.write(f"Occupancy: {data['current'][i]} / {data['max_capacity'][i]}")
            compliance = int(df.loc[i, "overall_compliance"])
            color = "🟢" if compliance >= 90 else "🟡" if compliance >= 80 else "🔴"
            st.write(f"Safety: {color} {compliance}%")
