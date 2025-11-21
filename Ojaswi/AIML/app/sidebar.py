import streamlit as st
from pathlib import Path

def load_sidebar():
    st.sidebar.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:6px 4px;">
      <img src="assets/logo.png" width="44" style="border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.6)"/>
      <div style="line-height:1;">
        <div style="font-weight:700;font-size:16px;">SafetyEye</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.75);">AI Workplace Safety</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('---')
    st.sidebar.title('Navigation')
    pages = ['Home', 'Live Monitor', 'Reports', 'Analytics', 'Settings']
    choice = st.sidebar.radio('', pages)

    st.sidebar.markdown('---')
    st.sidebar.markdown('**Quick Actions**')
    # show uploaded project PDF (local path you uploaded)
    pdf_path = Path('/mnt/data/Saftey_Eye.pdf')
    if pdf_path.exists():
        st.sidebar.markdown(f'[📄 View project spec]({pdf_path})')
    else:
        st.sidebar.markdown('Project spec not found at `/mnt/data/Saftey_Eye.pdf`')

    st.sidebar.markdown('---')
    st.sidebar.caption('Built with ❤️ by Oju — extract into your AIML folder and run.')
    return choice
