import streamlit as st


_custom_css = """
.main-header {
font-size: 2.1rem;
font-weight: bold;
color: #1f77b4;
text-align: center;
margin-bottom: 12px;
}
.metric-card {
background-color: #f0f2f6;
padding: 12px;
border-radius: 10px;
border-left: 5px solid #1f77b4;
}
.alert-box {
padding: 12px;
border-radius: 6px;
margin: 8px 0;
}
.alert-critical { background-color: #ffebee; border-left: 5px solid #f44336; }
.alert-warning { background-color: #fff3e0; border-left: 5px solid #ff9800; }
.alert-success { background-color: #e8f5e9; border-left: 5px solid #4caf50; }
"""




def inject_theme():
st.markdown(f"<style>{_custom_css}</style>", unsafe_allow_html=True)