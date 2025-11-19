import streamlit as st




def ensure_session_state():
if 'monitoring_active' not in st.session_state:
st.session_state.monitoring_active = False
if 'alerts' not in st.session_state:
st.session_state.alerts = []
# default placeholders for sidebar-driven values
st.session_state.zones = st.session_state.get('zones', ["Assembly Line A", "Warehouse", "Loading Dock"])
st.session_state.helmet_threshold = st.session_state.get('helmet_threshold', 90)
st.session_state.vest_threshold = st.session_state.get('vest_threshold', 85)
st.session_state.max_occupancy = st.session_state.get('max_occupancy', 50)