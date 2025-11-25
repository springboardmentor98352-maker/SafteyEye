import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🚧 SafetyEye</h2>", unsafe_allow_html=True)
        st.divider()

        st.page_link("app.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/1_Train_Model.py", label="🏋️ Train Model", icon="🧠")
        st.page_link("pages/2_Detection.py", label="🎥 Real-Time Detection", icon="🎥")
        st.page_link("pages/3_Analytics.py", label="📊 Analytics & Logs", icon="📊")
        st.page_link("pages/4_About.py", label="ℹ️ About Project", icon="❓")
