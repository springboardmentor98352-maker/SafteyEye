import streamlit as st
from components.ui import set_global_styles, sidebar_control_panel
from pages import live, analytics, alerts, people

st.set_page_config(
    page_title="SafetyEye – Workplace Safety Monitor",
    page_icon="🏭",
    layout="wide"
)

# global CSS + small JS helpers
set_global_styles()

# get state from sidebar (includes zones, max_capacity etc)
state = sidebar_control_panel()

# top header: cleaned — removed small "Project for GitHub demo" text
st.markdown(
    """
    <div class="header-wrapper" style="display:flex;align-items:center;gap:18px;padding:10px 4px 6px 4px;">
      <div style="font-size:36px;line-height:1">🏭</div>
      <div style="flex:1; pointer-events: none;">
        <h1 style="margin:0 0 4px 0; color: #e6eef8; font-weight:700; letter-spacing: -0.5px;">
          SafetyEye — Workplace Safety & Occupancy Monitor
        </h1>
        <div style="color:#aebfd9; margin-top:2px; font-size:14px;">Realtime safety insights • AI-style recommendations • Exportable reports</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

pages = {
    "Live Monitoring": live.app,
    "Analytics": analytics.app,
    "Alerts": alerts.app,
    "People Tracking": people.app
}

selected = st.sidebar.radio("Navigation", list(pages.keys()))
# call selected page
pages[selected](state)
