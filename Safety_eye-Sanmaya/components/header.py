import streamlit as st

def header():
    st.markdown(
        """
        <div class='header-container'>
            <h1>🚨 SafetyEye Workplace Safety Monitoring</h1>
            <p>AI-powered PPE Detection | Real-Time Alerts | Occupancy Insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )
