import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu

# Import pages
from app.pages import home, live_monitor, analytics, reports, settings


# ============================
# Load Custom CSS (Dark Theme)
# ============================
def load_css():
    css_path = "app/styles/theme.css"
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Failed to load theme.css: {e}")


# Streamlit Config
st.set_page_config(
    page_title="SafetyEye | PPE Monitoring",
    layout="wide",
    page_icon="🛡️",
)

load_css()


# ============================
# HEADER (Dark Top Navbar)
# ============================
st.markdown(
    """
    <div class="dark-navbar">
        <h2>🛡️ SafetyEye — PPE Monitoring System</h2>
        <p>AI-powered Helmet, Mask & Vest Violation Detection</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================
# SIDEBAR (Styled like UI screenshot)
# ============================
with st.sidebar:

    # Sidebar Title
    st.markdown("""
        <h2 style='padding-left: 10px; color: #d1d5db; margin-bottom: -5px;'>
            📝 Menu
        </h2>
        <hr style='border:1px solid #333;'>
    """, unsafe_allow_html=True)

    # Option Menu
    selected = option_menu(
        menu_title="",   # no title inside menu
        options=[
            "Home",
            "Live Monitor",
            "Analytics",
            "Reports",
            "Settings"
        ],
        icons=[
            "house-fill",
            "camera-video-fill",
            "bar-chart-fill",
            "file-earmark-text-fill",
            "gear-fill"
        ],
        default_index=0,
        orientation="vertical",

        styles={
            "container": {
                "padding": "10px 5px",
                "background-color": "#111827"
            },
            "icon": {
                "color": "#9CA3AF",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px",
                "color": "#E5E7EB",
                "padding": "12px 20px",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background-color": "#EF4444",
                "color": "white",
                "font-weight": "bold",
            }
        }
    )


# ============================
# PAGE ROUTING
# ============================
if selected == "Home":
    home.app()

elif selected == "Live Monitor":
    live_monitor.app()

elif selected == "Analytics":
    analytics.app()

elif selected == "Reports":
    reports.app()

elif selected == "Settings":
    settings.app()


