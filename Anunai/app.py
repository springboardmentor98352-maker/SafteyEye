#        py -3.11 -m streamlit run app.py

"""
app.py - SafetyEye Dashboard (entry point)

Folder layout expected:
SafetyEye-Dashboard/
  app.py
  requirements.txt
  core/
  pages/

Note: Project PDF (internship brief) is at /mnt/data/Saftey_Eye.pdf
"""

import streamlit as st
from pages import live_monitor, alerts, analytics

st.set_page_config(page_title="SafetyEye Dashboard", layout="wide", initial_sidebar_state="expanded")

PAGES = {
    "Live Monitor": live_monitor,
    "Alerts": alerts,
    "Analytics": analytics
}

# Sidebar - global controls & quick info
st.sidebar.title("SafetyEye")
st.sidebar.markdown("**Project brief:** `/mnt/data/Saftey_Eye.pdf`")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navigate", list(PAGES.keys()))

# Start / Stop global controls affect pages that watch st.session_state.running
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last_email_times" not in st.session_state:
    st.session_state.last_email_times = {}

start = st.sidebar.button("Start")
stop = st.sidebar.button("Stop")
if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False

st.sidebar.markdown("---")
st.sidebar.caption("Demo mode uses a simulator. Replace core/inference.py to plug YOLOv8 (TODO markers present).")

# Render selected page
PAGES[page].app()
