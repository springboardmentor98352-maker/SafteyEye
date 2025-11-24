import streamlit as st
from components.sidebar import sidebar
from components.header import header
from components.cards import display_cards

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="SafetyEye Dashboard",
    page_icon="🚨",
    layout="wide",
)

# ----------------- CUSTOM CSS LOAD -----------------
try:
    with open("assets/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ CSS file not found. Please verify assets/styles.css path.")

# ----------------- UI COMPONENTS -----------------
sidebar()      # Loads sidebar from components/sidebar.py
header()       # Loads header from components/header.py
display_cards()  # Loads card summaries

# ----------------- MAIN CONTENT -----------------
st.markdown("### 📍 System Overview")

st.write(
    """
    **SafetyEye** is an AI-powered workplace safety monitoring system designed to:
    - Detect PPE (helmet, vest, gloves, boots) compliance
    - Identify unsafe activities and hazards
    - Track workforce occupancy and attendance
    - Generate real-time alerts and safety analytics

    Use the navigation panel on the left to explore more features.
    """
)
