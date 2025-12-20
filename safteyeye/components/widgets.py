import streamlit as st
import pandas as pd

def kpi(label, value, subtitle=None, delta=None):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi'>{value}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='kpi-sub'>{subtitle}</div>", unsafe_allow_html=True)
    if delta is not None:
        st.write(f"Δ {delta}")
    st.markdown("</div>", unsafe_allow_html=True)

def styled_table(df: pd.DataFrame):
    st.dataframe(df, width="stretch")
