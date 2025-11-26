"""
app.py
Lightweight router for the refactored SafetyEye Streamlit app.
This module only handles page routing and session state; UI lives in `ui_home` and `ui_dashboard`.
"""

import streamlit as st

st.set_page_config(page_title="SafetyEye Dashboard", layout="wide", initial_sidebar_state="expanded")


# initialize routing state
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'


def go(page_name: str):
    """Set the current page and let Streamlit rerun to render the target view."""
    st.session_state['page'] = page_name


def main():
    page = st.session_state.get('page', 'home')
    if page == 'home':
        from ui_home import show_home

        show_home(go)
    else:
        from ui_dashboard import show_dashboard

        show_dashboard(go)


if __name__ == '__main__':
    main()
