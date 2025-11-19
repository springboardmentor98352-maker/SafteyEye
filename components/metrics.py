import streamlit as st
import numpy as np


def render_main_metrics(occupancy_data):
# occupancy_data is expected to be a dict with keys: zone, current, max_capacity, helmet_compliance, vest_compliance
col1, col2, col3, col4, col5 = st.columns(5)


total_occupancy = sum(occupancy_data['current']) if occupancy_data['current'] else 0
avg_helmet = int(np.mean(occupancy_data['helmet_compliance'])) if occupancy_data['helmet_compliance'] else 0
avg_vest = int(np.mean(occupancy_data['vest_compliance'])) if occupancy_data['vest_compliance'] else 0
active_violations = np.random.randint(0, 5)
zones_monitored = len(occupancy_data['zone'])


with col1:
st.metric("👥 Total Occupancy", total_occupancy, delta=f"{np.random.randint(-5, 10)} from avg")


with col2:
st.metric("🪖 Helmet Compliance", f"{avg_helmet}%", delta=f"{avg_helmet - st.session_state.helmet_threshold}%")


with col3:
st.metric("🦺 Vest Compliance", f"{avg_vest}%", delta=f"{avg_vest - st.session_state.vest_threshold}%")


with col4:
st.metric("⚠️ Active Violations", active_violations, delta=f"{np.random.randint(-2, 3)} from last hour")


with col5:
st.metric("📍 Zones Monitored", zones_monitored)