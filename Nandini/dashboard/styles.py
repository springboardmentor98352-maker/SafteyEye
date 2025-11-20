import streamlit as st

def load_css():
    st.markdown("""
    <style>
    body { background-color: #F5F7FA; }
    .metric-card {
        padding: 18px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #dbe2ef;
        text-align: center;
        margin-bottom: 12px;
    }
    .alert-card {
        padding: 12px;
        border-radius: 8px;
        background-color: #fff3f3;
        border-left: 5px solid #ff4d4d;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
