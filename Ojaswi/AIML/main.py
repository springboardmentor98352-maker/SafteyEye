import streamlit as st
from streamlit_option_menu import option_menu

# ----------- APP CONFIG -----------
st.set_page_config(
    page_title="SafetyEye | PPE Monitoring",
    layout="wide",
    page_icon="🛡️",
)

# ----------- DARK THEME CSS -----------
dark_css = """
<style>
body { background-color: #0d1117; color: white !important; }

[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}

.stButton>button {
    background-color: #238636 !important;
    color: white !important;
    border-radius: 5px;
}
.stButton>button:hover {
    background-color: #2ea043 !important;
}

.dataframe { color: white !important; }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)


# ----------- HEADER ----------
st.markdown("<h2 style='color:#58a6ff;'>🛡 SafetyEye — PPE Violation System</h2>", unsafe_allow_html=True)
st.write("---")


# ----------- SIDEBAR MENU --------
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Live Monitor", "Analytics", "Reports", "Settings"],
        icons=["house", "camera-video", "bar-chart", "file-earmark", "gear"],
        default_index=0
    )


# ----------- PAGE CONTROLLER --------
if selected == "Home":
    from app.pages.home import app as home_page
    home_page()

elif selected == "Live Monitor":
    from app.pages.live_monitor import app as live_page
    live_page()

elif selected == "Analytics":
    from app.pages.analytics import app as analytics_page
    analytics_page()

elif selected == "Reports":
    from app.pages.reports import app as reports_page
    reports_page()

elif selected == "Settings":
    from app.pages.settings import app as settings_page
    settings_page()
