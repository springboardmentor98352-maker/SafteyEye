# In pages/2_📈_analytics.py
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analytics - SafetyEye",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

# Show message if no data is available
if 'violations' not in st.session_state or not st.session_state.violations:
    st.info("No detection data available yet. Please run detections in the Live Monitoring or Image Detection page first.")
    st.stop()

# Convert violations to DataFrame for analysis
df = pd.DataFrame(st.session_state.violations)

# Convert timestamp to datetime if it's not already
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour

# Show basic stats
st.subheader("Detection Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Violations", len(df))
with col2:
    st.metric("Unique Violation Types", df['type'].nunique())
with col3:
    st.metric("Average Confidence", f"{df['confidence'].mean():.2%}")

# Show violation types distribution
if 'type' in df.columns:
    st.subheader("Violation Types")
    fig = px.pie(df, names='type', title='Distribution of Violation Types')
    st.plotly_chart(fig, use_container_width=True)

# Show violations over time
if 'timestamp' in df.columns:
    st.subheader("Violations Over Time")
    time_df = df.set_index('timestamp').resample('H').size().reset_index(name='count')
    fig = px.line(time_df, x='timestamp', y='count', title='Violations by Hour')
    st.plotly_chart(fig, use_container_width=True)