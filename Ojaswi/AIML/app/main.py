# defensive PYTHONPATH fix + main router
import sys, os
# ensure parent (AIML) is on path when Streamlit runs the script
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import streamlit as st
from pathlib import Path


# page config
st.set_page_config(page_title='SafetyEye — Breathtaking (Purple Galaxy)', layout='wide', page_icon='🛡️')

# load custom CSS
css_file = Path(__file__).parent / 'styles' / 'ui.css'
if css_file.exists():
    st.markdown(f'<style>{css_file.read_text()}</style>', unsafe_allow_html=True)

# load sidebar (returns page name)
from app.sidebar import load_sidebar
page = load_sidebar()

# route pages
if page == 'Home':
    from app.pages.home import app as home_app
    home_app()
elif page == 'Live Monitor':
    from app.pages.live_monitor import app as live_app
    live_app()
elif page == 'Reports':
    from app.pages.reports import app as reports_app
    reports_app()
elif page == 'Analytics':
    from app.pages.analytics import app as analytics_app
    analytics_app()
elif page == 'Settings':
    from app.pages.settings import app as settings_app
    settings_app()
else:
    st.error("Page not found")
