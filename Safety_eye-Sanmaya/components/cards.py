import streamlit as st

def display_cards():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='glass-card'><h3>👷 Workers Detected</h3><h2>42</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='glass-card'><h3>⛑ PPE Violations</h3><h2>3</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='glass-card'><h3>📊 Model Accuracy</h3><h2>91.2%</h2></div>", unsafe_allow_html=True)
