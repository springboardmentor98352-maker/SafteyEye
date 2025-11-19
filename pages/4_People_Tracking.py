import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.data_generator import generate_mock_data
from components.theme import inject_theme

# Apply global CSS UI theme
inject_theme()

st.title("👤 People Tracking & Movement Analytics")

# Load mock data (occupancy + historical)
occupancy_data, historical_data = generate_mock_data()

st.subheader("📊 Entry / Exit Flow (Last 24 Hours)")

# Create random sample entry/exit flow data
entry_exit_data = pd.DataFrame({
    'Hour': historical_data['time'],
    'Entries': np.random.randint(5, 20, 24),
    'Exits': np.random.randint(3, 18, 24)
})

# Flow line chart
fig_flow = go.Figure()
fig_flow.add_trace(go.Scatter(
    x=entry_exit_data['Hour'],
    y=entry_exit_data['Entries'],
    name='Entries',
    fill='tozeroy',
    mode='lines+markers'
))
fig_flow.add_trace(go.Scatter(
    x=entry_exit_data['Hour'],
    y=entry_exit_data['Exits'],
    name='Exits',
    fill='tozeroy',
    mode='lines+markers'
))

fig_flow.update_layout(
    xaxis_title="Time",
    yaxis_title="Count",
    hovermode='x unified',
    height=350
)

st.plotly_chart(fig_flow, use_container_width=True)

st.divider()

# --------------------------
# PEOPLE DISTRIBUTION PIE CHART
# --------------------------
st.subheader("📍 Current People Distribution Across Zones")

zones = occupancy_data['zone']
counts = occupancy_data['current']

dist_df = pd.DataFrame({
    "Zone": zones,
    "Count": counts
})

fig_dist = px.pie(
    dist_df,
    names='Zone',
    values='Count',
    hole=0.4,
    title="People Distribution"
)
fig_dist.update_layout(height=350)

st.plotly_chart(fig_dist, use_container_width=True)

st.divider()

# --------------------------
# DWELL TIME
# --------------------------
st.subheader("⏱️ Average Dwell Time by Zone")

dwell_df = pd.DataFrame({
    'Zone': zones,
    'Avg_Minutes': np.random.randint(20, 180, len(zones))
})

fig_dwell = px.bar(
    dwell_df,
    x='Zone',
    y='Avg_Minutes',
    color='Avg_Minutes',
    color_continuous_scale="Blues",
    title="Average Time Spent in Each Zone (minutes)"
)
fig_dwell.update_layout(height=350, showlegend=False)

st.plotly_chart(fig_dwell, use_container_width=True)

st.divider()

# --------------------------
# PEAK OCCUPANCY TIMES
# --------------------------
st.subheader("📈 Peak Occupancy Times")

peak_times = pd.DataFrame({
    'Time Slot': ['8–10 AM', '10–12 PM', '12–2 PM', '2–4 PM', '4–6 PM'],
    'Avg_Occupancy': np.random.randint(40, 100, 5)
})

fig_peak = px.line(
    peak_times,
    x='Time Slot',
    y='Avg_Occupancy',
    markers=True,
    line_shape='spline',
    title="Peak Occupancy Patterns"
)

fig_peak.update_layout(height=350)

st.plotly_chart(fig_peak, use_container_width=True)

st.success("People tracking analytics updated successfully.")