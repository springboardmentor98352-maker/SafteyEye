import streamlit as st
from components.sidebar import render_sidebar
from components.metrics import render_main_metrics
from components.theme import inject_theme
from utils.data_generator import generate_mock_data

# Page setup
st.set_page_config(
    page_title="Workplace Safety & Occupancy Monitoring System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom theme/styles
inject_theme()

# Shared sidebar across all pages
render_sidebar()

# Main header
st.markdown(
    '<div class="main-header">🏭 Workplace Safety & Occupancy Monitoring System</div>',
    unsafe_allow_html=True
)

# Generate mock data for homepage metrics
occupancy_data, historical_data = generate_mock_data()

# Display the top summary metrics
render_main_metrics(occupancy_data)

st.info("Use the left sidebar to access Live Monitoring, Analytics, Alerts, and People Tracking pages.")