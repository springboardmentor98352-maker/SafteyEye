# In app.py
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SafetyEye - Real-Time Safety & Occupancy Monitor",
    page_icon="👁️",
    layout="wide"
)

# Custom CSS to hide the default Streamlit menu and footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Page title
st.title("SafetyEye - Real-Time Safety & Occupancy Monitor")
st.markdown("---")

# Navigation buttons
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if st.button("📹 Go to Live Monitoring", use_container_width=True):
        st.switch_page("pages/1_📹_live_monitoring.py")
with col2:
    if st.button("🖼️ Image PPE Detection", use_container_width=True):
        st.switch_page("pages/4_🖼️_image_detection.py")
with col3:
    if st.button("📊 View Analytics", use_container_width=True):
        st.switch_page("pages/2_📈_analytics.py")
with col4:
    if st.button("📋 View Logs", use_container_width=True):
        st.switch_page("pages/3_📋_violation_logs.py")

# Add some space
st.markdown("<br>", unsafe_allow_html=True)

# Main content
st.markdown("""
### Welcome to SafetyEye Dashboard

Please use the buttons above to navigate to the desired section:
- **Live Monitoring**: View real-time safety monitoring with your YOLO model
- **Image PPE Detection**: Upload an image to detect PPE compliance and missing safety equipment
- **Analytics**: View detection statistics and trends
- **Logs**: Review past violations and detections
""")

# Add a footer
st.markdown("---")
st.caption("SafetyEye - AI-Powered Workplace Safety Monitoring")